"""
This test uses cases generated with the following C language code:

    #include <stdio.h>
    #include <stdint.h>

    typedef int32_t BME280_S32_t;
    typedef uint32_t BME280_U32_t;

    BME280_U32_t dig_T1 = 28353;
    BME280_S32_t dig_T2 = 26575;
    BME280_S32_t dig_T3 = 50;

    BME280_U32_t dig_P1 = 37446;
    BME280_S32_t dig_P2 = -10740;
    BME280_S32_t dig_P3 = 3024;
    BME280_S32_t dig_P4 = 8986;
    BME280_S32_t dig_P5 = -124;
    BME280_S32_t dig_P6 = -7;
    BME280_S32_t dig_P7 = 9900;
    BME280_S32_t dig_P8 = -10230;
    BME280_S32_t dig_P9 = 4285;

    BME280_U32_t dig_H1 = 0;
    BME280_S32_t dig_H2 = 354;
    BME280_U32_t dig_H3 = 0;
    BME280_S32_t dig_H4 = 340;
    BME280_S32_t dig_H5 = 0;
    BME280_S32_t dig_H6 = 30;

    // Returns temperature in DegC, double precision. Output value of “51.23” equals
    // 51.23 DegC. // t_fine carries fine temperature as global value
    BME280_S32_t t_fine;
    double BME280_compensate_T_double(BME280_S32_t adc_T) {
      double var1, var2, T;
      var1 = (((double)adc_T) / 16384.0 - ((double)dig_T1) / 1024.0) *
             ((double)dig_T2);
      var2 = ((((double)adc_T) / 131072.0 - ((double)dig_T1) / 8192.0) *
              (((double)adc_T) / 131072.0 - ((double)dig_T1) / 8192.0)) *
             ((double)dig_T3);
      t_fine = (BME280_S32_t)(var1 + var2);
      T = (var1 + var2) / 5120.0;
      return T;
    }
    // Returns pressure in Pa as double. Output value of “96386.2” equals 96386.2 Pa
    // = 963.862 hPa
    double BME280_compensate_P_double(BME280_S32_t adc_P) {
      double var1, var2, p;
      var1 = ((double)t_fine / 2.0) - 64000.0;
      var2 = var1 * var1 * ((double)dig_P6) / 32768.0;
      var2 = var2 + var1 * ((double)dig_P5) * 2.0;
      var2 = (var2 / 4.0) + (((double)dig_P4) * 65536.0);
      var1 = (((double)dig_P3) * var1 * var1 / 524288.0 + ((double)dig_P2) * var1) /
             524288.0;
      var1 = (1.0 + var1 / 32768.0) * ((double)dig_P1);
      if (var1 == 0.0) {
        return 0;  // avoid exception caused by division by zero
      }
      p = 1048576.0 - (double)adc_P;
      p = (p - (var2 / 4096.0)) * 6250.0 / var1;
      var1 = ((double)dig_P9) * p * p / 2147483648.0;
      var2 = p * ((double)dig_P8) / 32768.0;
      p = p + (var1 + var2 + ((double)dig_P7)) / 16.0;
      return p;
    }
    // Returns humidity in %rH as as double. Output value of “46.332” represents
    // 46.332 %rH
    double bme280_compensate_H_double(BME280_S32_t adc_H)
    {
      double var_H;
      var_H = (((double)t_fine) - 76800.0);
      var_H =
          (adc_H - (((double)dig_H4) * 64.0 + ((double)dig_H5) / 16384.0 * var_H)) *
          (((double)dig_H2) / 65536.0 *
           (1.0 +
            ((double)dig_H6) / 67108864.0 * var_H *
                (1.0 + ((double)dig_H3) / 67108864.0 * var_H)));
      var_H = var_H * (1.0 - ((double)dig_H1) * var_H / 524288.0);
      if (var_H > 100.0)
        var_H = 100.0;
      else if (var_H < 0.0)
        var_H = 0.0;
      return var_H;
    }

    void evaluate_curve(const char* name, double (*curve_fn) (BME280_S32_t), BME280_S32_t a, BME280_S32_t b)
    {
        printf("%s_values = (", name);
        for(int i = 0; i < 10; i += 1)
        {
            double t = (*curve_fn)(i * a + b);
            printf("%g, ", t);
        }
        printf(")\n");
    }

    int main(int argc, char** argv)
    {
        evaluate_curve("t", &BME280_compensate_T_double, 100000, 0);
        evaluate_curve("p", &BME280_compensate_P_double, 100000, 0);
        evaluate_curve("h", &bme280_compensate_H_double, 100000, 0);
    }

"""

from sagan.baro import Barometer


def assert_almost_equal(x, y, rel_tolerance=1e-4):
    if x == y == 0:
        return
    rel_diff = 2 * abs(x - y) / (x + y)
    assert rel_diff < rel_tolerance, "{0} != {1}, with relative tolerance {2}".format(x, y, rel_tolerance)


def test_calibration_curves():
    baro = Barometer(None, 0x00)
    baro.temperature_parameters[0] = 28353
    baro.temperature_parameters[1] = 26575
    baro.temperature_parameters[2] = 50

    baro.pressure_parameters[0] = 37446
    baro.pressure_parameters[1] = -10740
    baro.pressure_parameters[2] = 3024
    baro.pressure_parameters[3] = 8986
    baro.pressure_parameters[4] = -124
    baro.pressure_parameters[5] = -7
    baro.pressure_parameters[6] = 9900
    baro.pressure_parameters[7] = -10230
    baro.pressure_parameters[8] = 4285

    baro.humidity_parameters[0] = 0
    baro.humidity_parameters[1] = 354
    baro.humidity_parameters[2] = 0
    baro.humidity_parameters[3] = 340
    baro.humidity_parameters[4] = 0
    baro.humidity_parameters[5] = 30

    # The following lines are output by the C program at the start of this module
    t_a = 100000
    t_b = -100000
    t_values = (-175.221, -143.598, -111.964, -80.3188, -48.6621, -16.994, 14.6855, 46.3763, 78.0785, 109.792,)
    p_a = 100000
    p_b = -100000
    p_values = (168562, 151534, 134575, 117685, 100865, 84114.7, 67433.7, 50822.1, 34280, 17807.5,)
    h_a = 2100
    h_b = 21000
    h_values = (0, 7.40383, 19.0068, 30.6099, 42.2129, 53.8159, 65.4189, 77.0219, 88.6249, 100,)

    for i in range(10):
        t_raw = i * t_a + t_b
        p_raw = i * p_a + p_b
        h_raw = i * h_a + h_b
        t, p, h = baro.apply_calibration(t_raw, p_raw, h_raw, 25.0 * 5120)

        assert_almost_equal(t, t_values[i])
        assert_almost_equal(p, p_values[i])
        assert_almost_equal(h, h_values[i])
