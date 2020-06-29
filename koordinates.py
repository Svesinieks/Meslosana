import math

def deg2rad(angle):
  return (angle / 180) * math.pi


def rad2deg(radians):
  return radians * (180 / math.pi)


def LKSToLatLon(x, y) :
    # Ellipsoid model constants (actual values here are for WGS84)
    UTMScaleFactor = 0.9996
    sm_a = 6378137.0
    sm_b = 6356752.314140
    sm_EccSquared = 6.69437999013e-03

    x -= 500000.0
    # Pirmā atšķirība no WGS84 - Kilometriņš šurpu, kilometriņš turpu.
    y -= -6000000.0
    x /= UTMScaleFactor
    y /= UTMScaleFactor

    # Otrā atšķirība no WGS84 - Centrālais meridiāns ir citur.
    lambda0 = deg2rad(24)

    # Precalculate n (Eq. 10.18)
    n = (sm_a - sm_b) / (sm_a + sm_b)

    # Precalculate alpha_ (Eq. 10.22)
    # (Same as alpha in Eq. 10.17)
    alpha_ = ((sm_a + sm_b) / 2.0) * (1 + (pow(n, 2.0) / 4) + (pow(n, 4.0) / 64))

    # Precalculate y_ (Eq. 10.23)
    y_ = y / alpha_

    # Precalculate beta_ (Eq. 10.22)
    beta_ = (3.0 * n / 2.0) + (-27.0 * pow(n, 3.0) / 32.0) + (269.0 * pow(n, 5.0) / 512.0)

    # Precalculate gamma_ (Eq. 10.22)
    gamma_ = (21.0 * pow(n, 2.0) / 16.0) + (-55.0 * pow(n, 4.0) / 32.0)

    # Precalculate delta_ (Eq. 10.22)
    delta_ = (151.0 * pow(n, 3.0) / 96.0) + (-417.0 * pow(n, 5.0) / 128.0)

    # Precalculate epsilon_ (Eq. 10.22)
    epsilon_ = (1097.0 * pow(n, 4.0) / 512.0)

    # Now calculate the sum of the series (Eq. 10.21)
    phif = y_ + (beta_ * math.sin(2.0 * y_)) + (gamma_ * math.sin(4.0 * y_)) + (delta_ * math.sin(6.0 * y_)) + (epsilon_ * math.sin(8.0 * y_))

    #  Precalculate ep2
    ep2 = (pow(sm_a, 2.0) - math.pow(sm_b, 2.0)) / pow(sm_b, 2.0)

    # Precalculate cos (phif)
    cf = math.cos(phif)

    # Precalculate nuf2
    nuf2 = ep2 * pow(cf, 2.0)

    # Precalculate Nf and initialize Nfpow
    Nf = pow(sm_a, 2.0) / (sm_b * ((1 + nuf2)**0.5))
    Nfpow = Nf

    # Precalculate tf
    tf = math.tan(phif)
    tf2 = tf * tf
    tf4 = tf2 * tf2

    # Precalculate fractional coefficients for x**n in the equations below to simplify the expressions for latitude and longitude.
    x1frac = 1.0 / (Nfpow * cf)

    Nfpow *= Nf   # now equals Nf**2)
    x2frac = tf / (2.0 * Nfpow)

    Nfpow *= Nf  # now equals Nf**3)
    x3frac = 1.0 / (6.0 * Nfpow * cf)

    Nfpow *= Nf   # now equals Nf**4)
    x4frac = tf / (24.0 * Nfpow)

    Nfpow *= Nf  # now equals Nf**5)
    x5frac = 1.0 / (120.0 * Nfpow * cf)

    Nfpow *= Nf   # now equals Nf**6)
    x6frac = tf / (720.0 * Nfpow)

    Nfpow *= Nf   # now equals Nf**7)
    x7frac = 1.0 / (5040.0 * Nfpow * cf)

    Nfpow *= Nf;   # now equals Nf**8)
    x8frac = tf / (40320.0 * Nfpow)

    # Precalculate polynomial coefficients for x**n. -- x**1 does not have a polynomial coefficient.
    x2poly = -1.0 - nuf2

    x3poly = -1.0 - 2 * tf2 - nuf2

    x4poly = 5.0 + 3.0 * tf2 + 6.0 * nuf2 - 6.0 * tf2 * nuf2 - 3.0 * (nuf2 * nuf2) - 9.0 * tf2 * (nuf2 * nuf2)

    x5poly = 5.0 + 28.0 * tf2 + 24.0 * tf4 + 6.0 * nuf2 + 8.0 * tf2 * nuf2

    x6poly = -61.0 - 90.0 * tf2 - 45.0 * tf4 - 107.0 * nuf2 + 162.0 * tf2 * nuf2

    x7poly = -61.0 - 662.0 * tf2 - 1320.0 * tf4 - 720.0 * (tf4 * tf2)

    x8poly = 1385.0 + 3633.0 * tf2 + 4095.0 * tf4 + 1575 * (tf4 * tf2)

    # Calculate latitude
    lat = phif + x2frac * x2poly * (x * x) + x4frac * x4poly * pow(x, 4.0) + x6frac * x6poly * pow(x, 6.0) + x8frac * x8poly * pow(x, 8.0)

    #Calculate longitude
    lon = lambda0 + x1frac * x + x3frac * x3poly * pow(x, 3.0) + x5frac * x5poly * pow(x, 5.0) + x7frac * x7poly * pow(x, 7.0)

    return [rad2deg(lat), rad2deg(lon)]


