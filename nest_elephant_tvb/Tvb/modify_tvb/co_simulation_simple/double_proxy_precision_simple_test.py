# -*- coding: utf-8 -*-
#
#
#  TheVirtualBrain-Scientific Package. This package holds all simulators, and
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
from nest_elephant_tvb.Tvb.modify_tvb.co_simulation_simple.function_tvb import TvbSim
from tvb.tests.library.base_testcase import BaseTestCase
import numpy as np
import numpy.random as rgn


class TestDoubleProxyPrecisionSimple(BaseTestCase):
    def test_double_proxy_precision_simple(self):
        weight = np.array([[1, 1], [1, 1]])
        delay = np.array([[10.0, 10.0], [10.0, 10.0]])
        resolution_simulation = 0.1
        resolution_monitor = 0.1 * 3
        time_synchronize = 0.1 * 3
        proxy_id_1 = [0]
        proxy_id_2 = [1]

        # full simulation
        rgn.seed(42)
        sim_ref = TvbSim(weight, delay, [], resolution_simulation, resolution_monitor, time_synchronize)
        time, result_ref, s_ref = sim_ref(resolution_monitor, s=True)

        # simulation with one proxy
        rgn.seed(42)
        sim_1 = TvbSim(weight, delay, proxy_id_1, resolution_simulation, resolution_monitor, time_synchronize)
        time, result_1, s_1 = sim_1(resolution_monitor, [time, result_ref[:, proxy_id_1][:, :, 0]], s=True)

        # simulation_2 with one proxy
        rgn.seed(42)
        sim_2 = TvbSim(weight, delay, proxy_id_2, resolution_simulation, resolution_monitor, time_synchronize)
        time, result_2, s_2 = sim_2(resolution_monitor, [time, result_1[:, proxy_id_2][:, :, 0]], s=True)

        # COMPARE PROXY 1
        diff_1 = np.where(np.squeeze(result_ref, axis=2)[0] != np.squeeze(result_1, axis=2)[0])
        diff_s_1 = np.where(np.squeeze(s_ref, axis=2)[0] != np.squeeze(s_1, axis=2)[0])
        assert diff_1[0].size == 0
        assert diff_s_1[0].size == 0
        # COMPARE PROXY 2
        diff_2 = np.where(np.squeeze(result_ref, axis=2)[0] != np.squeeze(result_2, axis=2)[0])
        diff_s_2 = np.where(np.squeeze(s_ref, axis=2)[0] != np.squeeze(s_2, axis=2)[0])
        assert diff_2[0].size == 0
        assert diff_s_2[0].size == 0

        for i in range(0, 100):
            time, result_ref, s_ref = sim_ref(time_synchronize, s=True)
            time, result_1, s_1 = sim_1(time_synchronize, [time, result_ref[:, proxy_id_1][:, :, 0]], s=True)
            time, result_2, s_2 = sim_2(time_synchronize, [time, result_1[:, proxy_id_2][:, :, 0]], s=True)

            # COMPARE PROXY 1
            diff_1 = np.where(np.squeeze(result_ref, axis=2)[0] != np.squeeze(result_1, axis=2)[0])
            diff_s_1 = np.where(np.squeeze(s_ref, axis=2)[0] != np.squeeze(s_1, axis=2)[0])
            assert diff_1[0].size == 0
            assert diff_s_1[0].size == 0
            # COMPARE PROXY 2
            diff_2 = np.where(np.squeeze(result_ref, axis=2)[0] != np.squeeze(result_2, axis=2)[0])
            diff_s_2 = np.where(np.squeeze(s_ref, axis=2)[0] != np.squeeze(s_2, axis=2)[0])
            assert diff_2[0].size == 0
            assert diff_s_2[0].size == 0