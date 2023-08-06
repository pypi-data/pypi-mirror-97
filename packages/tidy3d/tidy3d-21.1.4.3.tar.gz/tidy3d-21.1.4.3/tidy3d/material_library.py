import math
from .material import Medium
from .dispersion import DispersionModel, Sellmeier, Lorentz
from .constants import C_0, HBAR


class cSi(Medium):
    """Crystalline silicon at 26 deg C.

    Refs:
    * A. Deinega, I. Valuev, B. Potapkin, and Y. Lozovik, Minimizing light
      reflection from dielectric textured surfaces,
      J. Optical Society of America A, 28, 770-77 (2011).
    * M. A. Green and M. Keevers, Optical properties of intrinsic silicon
      at 300 K, Progress in Photovoltaics, 3, 189-92 (1995).
    * C. D. Salzberg and J. J. Villa. Infrared Refractive Indexes of Silicon,
      Germanium and Modified Selenium Glass,
      J. Opt. Soc. Am., 47, 244-246 (1957).
    * B. Tatian. Fitting refractive-index data with the Sellmeier dispersion
      formula, Appl. Opt. 23, 4477-4485 (1984).
    """

    def __init__(self, variant=None):
        super().__init__(name="cSi")
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Deinega2011"

        if "SalzbergVilla1957" == variant:
            self.dispmod = Sellmeier(
                [
                    (10.6684293, 0.301516485 ** 2),
                    (0.0030434748, 1.13475115 ** 2),
                    (1.54133408, 1104 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 11.00, C_0 / 1.36)
        elif "Deinega2011" == variant:
            self.dispmod = Lorentz(
                self.eps,
                [
                    (8.000, 3.64 * C_0, 0),
                    (2.850, 2.76 * C_0, 0.063 * C_0),
                    (-0.107, 1.73 * C_0, 2.5 * C_0),
                ],
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.0, C_0 / 0.4)


class aSi(Medium):
    """Amorphous silicon

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="aSi")
        self.eps = 3.109
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(17.68 - self.eps, 3.93 * eV_to_Hz, 0.5 * 1.92 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)


class AlAs(Medium):
    """AlAs

    Refs:
    * R.E. Fern and A. Onton, J. Applied Physics, 42, 3499-500 (1971)
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="AlAs")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(8.27 - self.eps, 4.519 * eV_to_Hz, 0.5 * 0.378 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0 * eV_to_Hz, 3 * eV_to_Hz)
        elif "FernOnton1971" == variant:
            self.dispmod = Sellmeier(
                [
                    (6.0840, 0.2822 ** 2),
                    (1.900, 27.62 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 2.2, C_0 / 0.56)


class AlGaN(Medium):
    """AlGaN

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="AlGaN")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(4.6 - self.eps, 7.22 * eV_to_Hz, 0.5 * 0.127 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 4 * eV_to_Hz)


class AlN(Medium):
    """AlN

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="AlN")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(4.306 - self.eps, 8.916 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4.75 * eV_to_Hz)


class Al2O3(Medium):
    """Alumina

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="Al2O3")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.52 - self.eps, 12.218 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 6 * eV_to_Hz)


class AlxOy(Medium):
    """AlxOy

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="AlxOy")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps,
                [(3.171 - self.eps, 12.866 * eV_to_Hz, 0.5 * 0.861 * eV_to_Hz)],
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 6 * eV_to_Hz)


class Aminoacid(Medium):
    """Amino acid

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="Aminoacid")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(1.486 - self.eps, 14.822 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5 * eV_to_Hz)


class CaF2(Medium):
    """CaF2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="CaF2")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.036 - self.eps, 15.64 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4.75 * eV_to_Hz)


class GeOx(Medium):
    """GeOx

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="GeOx")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps,
                [(2.645 - self.eps, 16.224 * eV_to_Hz, 0.5 * 0.463 * eV_to_Hz)],
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 4 * eV_to_Hz)


class H2O(Medium):
    """Water

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="H2O")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(1.687 - self.eps, 11.38 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)


class HfO2(Medium):
    """HfO2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="HfO2")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.9 - self.eps, 9.4 * eV_to_Hz, 0.5 * 3.0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)


class HMDS(Medium):
    """HMDS

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="HMDS")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.1 - self.eps, 12.0 * eV_to_Hz, 0.5 * 0.5 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6.5 * eV_to_Hz)


class ITO(Medium):
    """Indium Tin Oxide

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="ITO")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.5 - self.eps, 6.8 * eV_to_Hz, 0.5 * 0.637 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6 * eV_to_Hz)


class MgF2(Medium):
    """MgF2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="MgF2")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(1.899 - self.eps, 16.691 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.8 * eV_to_Hz, 3.8 * eV_to_Hz)


class MgO(Medium):
    """MgO

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="MgO")
        self.eps = 11.232
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.599 - self.eps, 1.0 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5.5 * eV_to_Hz)


class PEI(Medium):
    """PEI

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="PEI")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.09 - self.eps, 12.0 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4.75 * eV_to_Hz)


class PEN(Medium):
    """PEN

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="PEN")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.466 - self.eps, 4.595 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 3.2 * eV_to_Hz)


class PET(Medium):
    """PET

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="PET")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.2 - self.eps, 7.0 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = None


class PMMA(Medium):
    """PMMA

    Refs:
    * N. Sultanova, S. Kasarova and I. Nikolov.
      Dispersion properties of optical polymers,
      Acta Physica Polonica A 116, 585-587 (2009)
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="PMMA")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Sultanova2009"

        if "Horiba" == variant:
            eV_to_Hz = 0.5 / (math.pi * HBAR)
            self.dispmod = Lorentz(
                self.eps, [(2.17 - self.eps, 11.427 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4.55 * eV_to_Hz)
        elif "Sultanova2009" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.1819, 0.011313),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.052, C_0 / 0.4368)


class Polycarbonate(Medium):
    """Polycarbonate

    Refs:
    * N. Sultanova, S. Kasarova and I. Nikolov.
      Dispersion properties of optical polymers,
      Acta Physica Polonica A 116, 585-587 (2009)
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="Polycarbonate")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Sultanova2009"

        if "Horiba" == variant:
            eV_to_Hz = 0.5 / (math.pi * HBAR)
            self.dispmod = Lorentz(
                self.eps, [(2.504 - self.eps, 12.006 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 4 * eV_to_Hz)
        elif "Sultanova2009" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.4182, 0.021304),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.052, C_0 / 0.4368)


class Polystyrene(Medium):
    """Polystyrene

    Refs:
    * N. Sultanova, S. Kasarova and I. Nikolov.
      Dispersion properties of optical polymers,
      Acta Physica Polonica A 116, 585-587 (2009)
    """

    def __init__(self, variant=None):
        super().__init__(name="Polystyrene")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Sultanova2009"

        if "Sultanova2009" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.4435, 0.020216),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.052, C_0 / 0.4368)


class Cellulose(Medium):
    """Cellulose

    Refs:
    * N. Sultanova, S. Kasarova and I. Nikolov.
      Dispersion properties of optical polymers,
      Acta Physica Polonica A 116, 585-587 (2009)
    """

    def __init__(self, variant=None):
        super().__init__(name="Cellulose")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Sultanova2009"

        if "Sultanova2009" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.124, 0.011087),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.052, C_0 / 0.4368)


class pSi(Medium):
    """pSi

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="pSi")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(12.0 - self.eps, 4.0 * eV_to_Hz, 0.5 * 0.5 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5 * eV_to_Hz)


class PTFE(Medium):
    """PTFE

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="PTFE")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(1.7 - self.eps, 16.481 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 6.5 * eV_to_Hz)


class PVC(Medium):
    """PVC

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="PVC")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.304 - self.eps, 12.211 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 4.75 * eV_to_Hz)


class Sapphire(Medium):
    """Sapphire

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="Sapphire")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.09 - self.eps, 13.259 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5.5 * eV_to_Hz)


class SiC(Medium):
    """SiC

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="SiC")
        self.eps = 3.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(6.8 - self.eps, 8.0 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 4 * eV_to_Hz)


class SiN(Medium):
    """SiN

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="SiN")
        self.eps = 2.32
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.585 - self.eps, 6.495 * eV_to_Hz, 0.5 * 0.398 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 6 * eV_to_Hz)


class Si3N4(Medium):
    """Si3N4

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    * H. R. Philipp. Optical properties of silicon nitride, J. Electrochim. Soc. 120, 295-300 (1973)
    * T. Baak. Silicon oxynitride; a material for GRIN optics, Appl. Optics 21, 1069-1072 (1982)
    * K. Luke, Y. Okawachi, M. R. E. Lamont, A. L. Gaeta, M. Lipson.
      Broadband mid-infrared frequency comb generation in a Si3N4 microresonator,
      Opt. Lett. 40, 4823-4826 (2015)
    """

    def __init__(self, variant=None):
        super().__init__(name="Si3N4")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(5.377 - self.eps, 3.186 * eV_to_Hz, 0.5 * 1.787 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 5.5 * eV_to_Hz)
        elif "Philipp1973" == variant:
            self.dispmod = Sellmeier(
                [
                    (2.8939, 0.13967 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 1.24, C_0 / 0.207)
        elif "Luke2015" == variant:
            self.dispmod = Sellmeier(
                [
                    (3.0249, 0.1353406 ** 2),
                    (40314, 1239.842 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 5.504, C_0 / 0.31)


class SiO2(Medium):
    """SiO2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="SiO2")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.12 - self.eps, 12.0 * eV_to_Hz, 0.5 * 0.1 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.7 * eV_to_Hz, 5 * eV_to_Hz)


class SiON(Medium):
    """SiON

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="SiON")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.342 - self.eps, 10.868 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 3 * eV_to_Hz)


class Ta2O5(Medium):
    """Ta2O5

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="Ta2O5")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(4.133 - self.eps, 7.947 * eV_to_Hz, 0.5 * 0.814 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.75 * eV_to_Hz, 4 * eV_to_Hz)


class TiOx(Medium):
    """TiOx

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="TiOx")
        self.eps = 0.29
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.82 - self.eps, 6.5 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (0.6 * eV_to_Hz, 3 * eV_to_Hz)


class Y2O3(Medium):
    """Y2O3

    Refs:
    * Y. Nigara. Measurement of the optical constants of yttrium oxide,
      Jpn. J. Appl. Phys. 7, 404-408 (1968)
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="Y2O3")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Nigara1968"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(2.715 - self.eps, 9.093 * eV_to_Hz, 0.5 * 0 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.55 * eV_to_Hz, 4 * eV_to_Hz)
        elif "Nigara1968" == variant:
            self.dispmod = Sellmeier(
                [
                    (2.578, 0.1387 ** 2),
                    (3.935, 22.936 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 9.6, C_0 / 0.25)


class ZrO2(Medium):
    """ZrO2

    Refs:
    * Horiba Technical Note 08: Lorentz Dispersion Model
      http://www.horiba.com/fileadmin/uploads/Scientific/Downloads/OpticalSchool_CN/TN/ellipsometer/Lorentz_Dispersion_Model.pdf
    """

    def __init__(self, variant=None):
        super().__init__(name="ZrO2")
        self.eps = 1.0
        self.sigma = 0

        if variant is None:
            variant = "Horiba"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Horiba" == variant:
            self.dispmod = Lorentz(
                self.eps, [(3.829 - self.eps, 9.523 * eV_to_Hz, 0.5 * 0.128 * eV_to_Hz)]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (1.5 * eV_to_Hz, 3 * eV_to_Hz)


class BK7(Medium):
    """N-BK7 borosilicate glass"""

    def __init__(self, variant=None):
        super().__init__(name="BK7")
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Zemax"

        if "Zemax" == variant:
            self.dispmod = Sellmeier(
                [
                    (1.03961212, 0.00600069867),
                    (0.231792344, 0.0200179144),
                    (1.01046945, 103.560653),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 2.5, C_0 / 0.3)


class FusedSilica(Medium):
    """Fused silica

    Refs:
    * I. H. Malitson. Interspecimen comparison of the refractive index of
      fused silica, J. Opt. Soc. Am. 55, 1205-1208 (1965)
    * C. Z. Tan. Determination of refractive index of silica glass for
      infrared wavelengths by IR spectroscopy,
      J. Non-Cryst. Solids 223, 158-163 (1998)
    """

    def __init__(self, variant=None):
        super().__init__(name="FusedSilica")
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Zemax"

        if "Zemax" == variant:
            self.dispmod = Sellmeier(
                [
                    (0.6961663, 0.0684043 ** 2),
                    (0.4079426, 0.1162414 ** 2),
                    (0.8974794, 9.896161 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 6.7, C_0 / 0.21)


class GaAs(Medium):
    """Gallium arsenide

    Refs:
    * T. Skauli, P. S. Kuo, K. L. Vodopyanov, T. J. Pinguet, O. Levi,
      L. A. Eyres, J. S. Harris, M. M. Fejer, B. Gerard, L. Becouarn,
      and E. Lallier. Improved dispersion relations for GaAs and
      applications to nonlinear optics, J. Appl. Phys., 94, 6447-6455 (2003)
    """

    def __init__(self, variant=None):
        super().__init__(name="GaAs")
        self.eps = 5.372514
        self.sigma = 0

        if variant is None:
            variant = "Skauli2003"

        if "Skauli2003" == variant:
            self.dispmod = Sellmeier(
                [
                    (5.466742, 0.4431307 ** 2),
                    (0.02429960, 0.8746453 ** 2),
                    (1.957522, 36.9166 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 17, C_0 / 0.97)


class Ag(Medium):
    """Silver.

    Refs:
    * A. D. Rakic et al., Applied Optics, 37, 5271-5283 (1998)
    """

    def __init__(self, variant=None):
        super().__init__(name="Ag")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (-2.502e-2 - 8.626e-3j, 5.987e-1 + 4.195e3j),
                    (-2.021e-1 - 9.407e-1j, -2.211e-1 + 2.680e-1j),
                    (-1.467e1 - 1.338e0j, -4.240e0 + 7.324e2j),
                    (-2.997e-1 - 4.034e0j, 6.391e-1 - 7.186e-2j),
                    (-1.896e0 - 4.808e0j, 1.806e0 + 4.563e0j),
                    (-9.396e0 - 6.477e0j, 1.443e0 - 8.219e1j),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (0.1 / h, 5 / h)


class Au(Medium):
    """Gold

    Refs:
    * P. B. Johnson and R. W. Christy. Optical constants of the noble metals, Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self, variant=None):
        super().__init__(name="Au")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-0.026955750077564202 - 0.0988664675659672j),
                        (0.447862536287849 + 359.3693488468651j),
                    ),
                    (
                        (-0.0938891003729386 - 0.4454781163574038j),
                        (-0.7634247243395327 + 3.3378646350288284j),
                    ),
                    (
                        (-0.10241859347785529 - 0.5861784202506137j),
                        (-0.5730996408150796 + 1.5750521669295217j),
                    ),
                    (
                        (-0.5859182121732974 - 2.8095998031643212j),
                        (1.1615305933022986 + 1.529923046941579j),
                    ),
                    (
                        (-2.3648208922948224 - 3.9506663577511176j),
                        (0.4781454204246356 + 10.004764935068316j),
                    ),
                    (
                        (-7.3871945816024915 - 16.048308950027597j),
                        (-3.046940555919119 + 20.73681036538383j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (0.64 / h, 6.6 / h)


class Cu(Medium):
    """Copper

    Refs:
    * P. B. Johnson and R. W. Christy. Optical constants of the noble metals, Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self, variant=None):
        super().__init__(name="Cu")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-0.01754034345120948 - 0.09123699694321295j),
                        (1.0330679957113091 + 356.1912618343321j),
                    ),
                    (
                        (-0.24469644728696058 - 0.16210178020229618j),
                        (-2.115558633152502 + 44.859580087846396j),
                    ),
                    (
                        (-0.4803840208384017 - 2.427821690986015j),
                        (1.3001522133543062 + 2.023013643197286j),
                    ),
                    (
                        (-2.094057267645235 - 4.0383221076029505j),
                        (3.349640664807941 + 8.362216588586927j),
                    ),
                    (
                        (-0.026387014517946214 - 19.200499737531043j),
                        (0.8222623812428774 + 5.49248564124662j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (0.64 / h, 6.6 / h)


class Al(Medium):
    """Aluminum

    Refs:
    * A. D. Rakic. Algorithm for the determination of intrinsic optical
      constants of metal films: application to aluminum,
      Appl. Opt. 34, 4755-4767 (1995)
    """

    def __init__(self, variant=None):
        super().__init__(name="Al")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-0.02543000644123838 - 0.03177449689697393j),
                        (2.655977979367176 + 1866.6744251245625j),
                    ),
                    (
                        (-0.0009040206995601725 + 0j),
                        (50.22383221124015 + 148.23535689736036j),
                    ),
                    (
                        (-7.083800421248227 - 0.5265552916184757j),
                        (-10.063691398117694 + 31.243557348153914j),
                    ),
                    (
                        (-0.11804263462150097 - 0.16034526808256572j),
                        (-30.44469672627293 + 50.702553768652265j),
                    ),
                    (
                        (-6.701254199352449 - 3.6481762896415066j),
                        (-11.175149154124156 - 9.307675442873656j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (0.1 / h, 10 / h)


class Be(Medium):
    """Beryllium

    Refs:
    * A. D. Rakic. Algorithm for the determination of intrinsic optical
      constants of metal films: application to aluminum,
      Appl. Opt. 34, 4755-4767 (1995)
    """

    def __init__(self, variant=None):
        super().__init__(name="Be")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-0.01467559642300368 - 0.011921713664657874j),
                        (11.102858393689859 + 997.3989259045288j),
                    ),
                    (
                        (-0.007192297005355153 + 0j),
                        (9.17076421804364 + 29779.653005475455j),
                    ),
                    (
                        (-0.1842186369882607 - 0.008345826991602062j),
                        (-12.613037097613995 - 289.8708706194137j),
                    ),
                    (
                        (-1.60693994861672 + 0j),
                        (24.140400506941724 + 84.04918080253373j),
                    ),
                    (
                        (-6.967518750932778 - 6.432541981234564j),
                        (-70.75228325846311 + 4.991406069340526j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (0.1 / h, 10 / h)


class Cr(Medium):
    """Chromium

    Refs:
    * A. D. Rakic. Algorithm for the determination of intrinsic optical
      constants of metal films: application to aluminum,
      Appl. Opt. 34, 4755-4767 (1995)
    """

    def __init__(self, variant=None):
        super().__init__(name="Cr")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-0.016744051287845056 - 0.030599362407448455j),
                        (1.5750990207513889 + 236.7100840009308j),
                    ),
                    (
                        (-0.0006926119317860557 + 0j),
                        (13.079639909964918 + 9.498414578099634j),
                    ),
                    (
                        (-0.38748596542834807 - 0.0005273528816316377j),
                        (-14.021929013546274 + 7.538522210064633j),
                    ),
                    (
                        (-1.4809291078222508 - 1.069387688480274j),
                        (0.008744427110544486 + 70.19584519933676j),
                    ),
                    (
                        (-2.181588953284235 - 9.966499320360377j),
                        (-3.262279485359157 - 2.873566458391711j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (0.1 / h, 10 / h)


class Ni(Medium):
    """Nickel

    Refs:
    * P. B. Johnson and R. W. Christy. Optical constants of the noble metals, Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self, variant=None):
        super().__init__(name="Ni")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-8.566496800121943e-08 - 0.09838278383411603j),
                        (0.049200052758942875 + 198.13631259069095j),
                    ),
                    (
                        (-0.018141304521375 - 0.10893544701556669j),
                        (5.318590644585675 - 12.472022072681165j),
                    ),
                    (
                        (-0.14928684097140146 - 0.0002279992692829006j),
                        (8.152053607665009 - 8.728651907340463j),
                    ),
                    (
                        (-0.645702819628624 - 0.6004225851474665j),
                        (-0.5915912865455546 + 15.891474422519119j),
                    ),
                    (
                        (-3.0851746199407315 - 5.908453169642721j),
                        (-3.8492168295859273 + 5.786796038682027j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (0.64 / h, 6.6 / h)


class Pd(Medium):
    """Palladium

    Refs:
    * P. B. Johnson and R. W. Christy. Optical constants of the noble metals, Phys. Rev. B 6, 4370-4379 (1972)
    """

    def __init__(self, variant=None):
        super().__init__(name="Pd")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-0.018395445268754196 - 0.05793104383593875j),
                        (-0.07689288540916725 + 291.6738427964993j),
                    ),
                    (
                        (-0.027922168600007236 + 0j),
                        (13.774347280659224 - 152.8766207180748j),
                    ),
                    (
                        (-0.760968579570245 - 0.30266586405836354j),
                        (-1.4518130571271635 + 38.71729641003975j),
                    ),
                    (
                        (-0.011091203757874 - 0.01312856138430063j),
                        (-1.4773982002493897 + 147.43877687698034j),
                    ),
                    (
                        (-6.690929831759696 - 4.077751585426895j),
                        (-5.714726349367318 - 1.64330224870603j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (0.64 / h, 6.6 / h)


class Pt(Medium):
    """Platinum

    Refs:
    * W. S. M. Werner, K. Glantschnig, C. Ambrosch-Draxl.
      Optical constants and inelastic electron-scattering data for 17
      elemental metals, J. Phys Chem Ref. Data 38, 1013-1092 (2009)
    """

    def __init__(self, variant=None):
        super().__init__(name="Pt")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-0.06695203438147745 - 0.14639101632437196j),
                        (3.1173416750016854 + 470.3702792275117j),
                    ),
                    (
                        (-0.05139078154733537 - 0.0398067193616464j),
                        (3.5905379829178328 + 290.51219463657986j),
                    ),
                    (
                        (-4.2702391463452 - 0.1023450079932173j),
                        (3.5169977232897742 + 136.11580292584603j),
                    ),
                    (
                        (-1.5016435398388222 - 0.042541250379806j),
                        (-1.2707409899595357 - 317.59660467815365j),
                    ),
                    (
                        (-6.560611329539 - 2.6604757095535057j),
                        (-0.3302567102379078 + 45.30726384867861j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (C_0 / 0.1, C_0 / 2.48)


class Ti(Medium):
    """Titanium

    Refs:
    * W. S. M. Werner, K. Glantschnig, C. Ambrosch-Draxl.
      Optical constants and inelastic electron-scattering data for 17
      elemental metals, J. Phys Chem Ref. Data 38, 1013-1092 (2009)
    """

    def __init__(self, variant=None):
        super().__init__(name="Ti")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-5.0904093494224216e-05 - 0.13324128147817416j),
                        (-9.262460287562153 + 357.0413551173238j),
                    ),
                    (-0.021305639299682624j, (20.1441560339523 + 13.91885088268019j)),
                    (
                        (-0.05721949014920069 - 0.041292872452438255j),
                        (-5.546364792564378 + 170.84002769123097j),
                    ),
                    (
                        (-3.5847638867645655 - 3.8101711951435884j),
                        (6.0646767851686985 + 5.5853872618611105j),
                    ),
                    (
                        (-0.002740508761501106 - 26.82270480785415j),
                        (1.7035181259573562 - 0.00606963757710623j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (C_0 / 0.1, C_0 / 2.48)


class W(Medium):
    """Tungsten

    Refs:
    * W. S. M. Werner, K. Glantschnig, C. Ambrosch-Draxl.
      Optical constants and inelastic electron-scattering data for 17
      elemental metals, J. Phys Chem Ref. Data 38, 1013-1092 (2009)
    """

    def __init__(self, variant=None):
        super().__init__(name="W")
        self.eps = 1
        self.sigma = 0

        h = HBAR
        self.dispmod = DispersionModel(
            poles=[
                (a / h, c / h)
                for (a, c) in [
                    (
                        (-0.003954896347816251 - 0.1802335610343007j),
                        (1.8921628775430088 + 418.28416384593686j),
                    ),
                    (
                        (-0.012319513432616953 - 0.0052557601183450126j),
                        (1.756799582125415 + 92.88601294383525j),
                    ),
                    (
                        (-5.0741907106627835 - 0.04234993352459908j),
                        (0.3303495961778782 + 36.26799302329413j),
                    ),
                    (
                        (-0.21756967367414215 - 0.9365555173092157j),
                        (0.38496157871304104 + 24.119535838621516j),
                    ),
                    (
                        (-2.6258028910978863 - 2.6236924266577835j),
                        (-0.23193732824781174 + 41.62320103829054j),
                    ),
                ]
            ]
        )
        self.poles = self.dispmod._poles
        self.frequency_range = (C_0 / 0.1, C_0 / 2.48)


class InP(Medium):
    """Indium Phosphide

    Refs:
    * G. D. Pettit and W. J. Turner. Refractive index of InP,
      J. Appl. Phys. 36, 2081 (1965)
    * A. N. Pikhtin and A. D. Yaskov. Disperson of the refractive index of
      semiconductors with diamond and zinc-blende structures,
      Sov. Phys. Semicond. 12, 622-626 (1978)
    * Handbook of Optics, 2nd edition, Vol. 2. McGraw-Hill 1994
    """

    def __init__(self, variant=None):
        super().__init__(name="InP")
        self.eps = 7.255
        self.sigma = 0

        if variant is None:
            variant = "Pettit1965"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Pettit1965" == variant:
            self.dispmod = Sellmeier(
                [
                    (2.316, 0.6263 ** 2),
                    (2.765, 32.935 ** 2),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 10, C_0 / 0.95)


class Ge(Medium):
    """Germanium

    Refs:
    * Icenogle et al.. Refractive indexes and temperature coefficients of
      germanium and silicon Appl. Opt. 15 2348-2351 (1976)
    * N. P. Barnes and M. S. Piltch. Temperature-dependent Sellmeier
      coefficients and nonlinear optics average power limit for germanium
      J. Opt. Soc. Am. 69 178-180 (1979)
    """

    def __init__(self, variant=None):
        super().__init__(name="Ge")
        self.eps = 9.28156
        self.sigma = 0

        if variant is None:
            variant = "Icenogle1976"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Icenogle1976" == variant:
            self.dispmod = Sellmeier(
                [
                    (6.72880, 0.44105),
                    (0.21307, 3870.1),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 12, C_0 / 2.5)


class YAG(Medium):
    """Yttrium aluminium garnet

    Refs:
    * D. E. Zelmon, D. L. Small and R. Page.
      Refractive-index measurements of undoped yttrium aluminum garnet
      from 0.4 to 5.0 um, Appl. Opt. 37, 4933-4935 (1998)
    """

    def __init__(self, variant=None):
        super().__init__(name="YAG")
        self.eps = 1
        self.sigma = 0

        if variant is None:
            variant = "Zelmon1998"

        eV_to_Hz = 0.5 / (math.pi * HBAR)
        if "Zelmon1998" == variant:
            self.dispmod = Sellmeier(
                [
                    (2.28200, 0.01185),
                    (3.27644, 282.734),
                ]
            )
            self.poles = self.dispmod._poles
            self.frequency_range = (C_0 / 5, C_0 / 0.4)
