# ========================================================
# AGRISENSE IOT - SENSOR CALIBRATION MATRIX (SHT31 & MQ-135)
# Target: MicroPython ESP32 / Sahel Thermal Compensation
# Author: AgriSense Engineering (Gombe State, Nigeria)
# ========================================================

class SensorCalibrationMatrix:
    """Provides temperature-compensated gas conversion for Sahel climate conditions"""
    
    @staticmethod
    def compensate_temperature(raw_temp, offset=-0.15):
        """Medical-grade Sensirion SHT31 offset adjustment"""
        return round(raw_temp + offset, 2)

    @staticmethod
    def mq135_rs_ro_ratio(raw_adc, v_in=3.3):
        """Calculate RS/RO ratio for MQ-135 ammonia gas sensor"""
        v_out = (raw_adc / 4095.0) * v_in
        if v_out == 0:
            return 10.0
        rs = ((v_in - v_out) / v_out) * 10.0 # 10k RL resistor
        ro = 10.0 # Baseline clean air resistance in k-ohms
        return round(rs / ro, 3)

    @staticmethod
    def calculate_ammonia_ppm(rs_ro_ratio, temp_c=30.0):
        """Convert RS/RO ratio into PPM with ambient temperature compensation"""
        # Polynomial approximation tuned for broiler deep litter pens
        temp_factor = 1.0 + ((temp_c - 20.0) * 0.008)
        base_ppm = 102.2 * (rs_ro_ratio ** -2.47)
        return round(base_ppm * temp_factor, 2)

if __name__ == "__main__":
    matrix = SensorCalibrationMatrix()
    ratio = matrix.mq135_rs_ro_ratio(1250)
    ppm = matrix.calculate_ammonia_ppm(ratio, temp_c=32.5)
    print(f"[CALIBRATION] MQ-135 RS/RO: {ratio} | Calibrated Ammonia: {ppm} PPM")
