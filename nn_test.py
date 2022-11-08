########################################
# CS63: Artificial Intelligence, Lab 5
# Fall 2022, Swarthmore College
########################################

import unittest
import neural_net as NN
from numpy import allclose, arange

class ApproximateTester(unittest.TestCase):
    def assertClose(self, actual, expected, rtol=1e-5, message=""):
        self.assertTrue(allclose(actual, expected, rtol),
                        (message + "\nactual={} and expected={} are not " +
                        "within tolerance={}").format(actual, expected, rtol))

class Test_Sigmoid(ApproximateTester):
    def setUp(self):
        self.layer5 = [NN.Node("l5-"+str(i)) for i in range(5)]
        self.layer10 = [NN.Node("l10-"+str(i)) for i in range(10)]
        for a,n in zip(arange(0, 1.1, .25), self.layer5):
            n.activation = a
        for d,n in zip(arange(-.125, .126, 1./16), self.layer5):
            n.delta = d
        for a,n in zip(arange(.05, .96, 0.1), self.layer10):
            n.activation = a
        for d,n in zip(arange(-.112,.12,.025), self.layer10):
            n.delta = d
        self.node55 = NN.SigmoidNode("n55")
        self.node510 = NN.SigmoidNode("n510")
        self.node105 = NN.SigmoidNode("n105")
        self.node1010 = NN.SigmoidNode("n1010")
        for i,n in zip(arange(-1,3.1), self.layer5):
            e = NN.Edge(n, self.node55, lambda: i)
            e.old_weight = e.weight
            self.node55.in_edges.append(e)
            e = NN.Edge(self.node55, n, lambda: -i)
            e.old_weight = e.weight
            self.node55.out_edges.append(e)
        for i,n in zip(arange(-.2,.61,.2), self.layer5):
            e = NN.Edge(n, self.node55, lambda: -i)
            e.old_weight = e.weight
            self.node510.in_edges.append(e)
            e = NN.Edge(self.node55, n, lambda: i)
            e.old_weight = e.weight
            self.node105.out_edges.append(e)
        for i,n in zip(arange(-.56,.17,.08), self.layer10):
            e = NN.Edge(n, self.node55, lambda: i)
            e.old_weight = e.weight
            self.node105.in_edges.append(e)
            e = NN.Edge(self.node55, n, lambda: -i)
            e.old_weight = e.weight
            self.node510.out_edges.append(e)
        for i,n in zip(arange(-.25,.66,.1), self.layer10):
            e = NN.Edge(n, self.node55, lambda: -i)
            e.old_weight = e.weight
            self.node1010.in_edges.append(e)
            e = NN.Edge(self.node55, n, lambda: i)
            e.old_weight = e.weight
            self.node1010.out_edges.append(e)

    def test_activation55(self):
        self.node55.compute_activation()
        expected = 0.99330714907571527
        self.assertClose(self.node55.activation, expected, message=
                         "SigmoidNode.compute_activation error.")
    def test_activation510(self):
        self.node510.compute_activation()
        expected = 0.2689414213699951
        self.assertClose(self.node510.activation, expected, message=
                         "SigmoidNode.compute_activation error.")
    def test_activation105(self):
        self.node105.compute_activation()
        expected = 0.4158094770645927
        self.assertClose(self.node105.activation, expected, message=
                         "SigmoidNode.compute_activation error.")
    def test_activation1010(self):
        self.node1010.compute_activation()
        expected = 0.13883499354730708
        self.assertClose(self.node1010.activation, expected, message=
                         "SigmoidNode.compute_activation error.")

    def test_output_delta55(self):
        self.node55.compute_activation()
        self.node55.compute_output_delta(0.0)
        expected = -0.0066035622185562385
        self.assertClose(self.node55.delta, expected, message=
                         "SigmoidNode.compute_output_delta error.")
        self.node55.compute_output_delta(1.0)
        expected = 4.4494452233794356e-05
        self.assertClose(self.node55.delta, expected, message=
                         "SigmoidNode.compute_output_delta error.")
    def test_output_delta510(self):
        self.node510.compute_activation()
        self.node510.compute_output_delta(0.0)
        expected = -0.052877092784266715
        self.assertClose(self.node510.delta, expected, message=
                         "SigmoidNode.compute_output_delta error.")
        self.node510.compute_output_delta(1.0)
        expected = 0.14373484045721513
        self.assertClose(self.node510.delta, expected, message=
                         "SigmoidNode.compute_output_delta error.")
    def test_output_delta105(self):
        self.node105.compute_activation()
        self.node105.compute_output_delta(0.0)
        expected = -0.1010050933338372
        self.assertClose(self.node105.delta, expected, message=
                         "SigmoidNode.compute_output_delta error.")
        self.node105.compute_output_delta(1.0)
        expected = 0.14190686251402546
        self.assertClose(self.node105.delta, expected, message=
                         "SigmoidNode.compute_output_delta error.")
    def test_output_delta1010(self):
        self.node1010.compute_activation()
        self.node1010.compute_output_delta(0.0)
        expected = -0.016599089353077918
        self.assertClose(self.node1010.delta, expected, message=
                         "SigmoidNode.compute_output_delta error.")
        self.node1010.compute_output_delta(1.0)
        expected = 0.10296074876094835
        self.assertClose(self.node1010.delta, expected, message=
                         "SigmoidNode.compute_output_delta error.")

    def test_hidden_delta55(self):
        self.node55.compute_activation()
        self.node55.compute_hidden_delta()
        expected = -0.0041550354192437704
        self.assertClose(self.node55.delta, expected, message=
                         "SigmoidNode.compute_hidden_delta error.")
    def test_hidden_delta510(self):
        self.node510.compute_activation()
        self.node510.compute_hidden_delta()
        expected = -0.032244357051603029
        self.assertClose(self.node510.delta, expected, message=
                         "SigmoidNode.compute_hidden_delta error.")
    def test_hidden_delta55(self):
        self.node105.compute_activation()
        self.node105.compute_hidden_delta()
        expected = 0.030363994480982832
        self.assertClose(self.node510.delta, expected, message=
                         "SigmoidNode.compute_hidden_delta error.")
    def test_hidden_delta55(self):
        self.node1010.compute_activation()
        self.node1010.compute_hidden_delta()
        expected = 0.024778776449131963
        self.assertClose(self.node1010.delta, expected, message=
                         "SigmoidNode.compute_hidden_delta error.")

class Test_Network(ApproximateTester):
    def test_predict_small(self):
        nn = NN.Network(3, 3, [3], weight_scale=10, random_seed=74)
        input_vector = [-1, 0, 1]
        target_vector = [7.9153787496713187e-08, 0.041550054491001708,
                         0.99999753053427387]
        output_vector = nn.predict(input_vector)
        self.assertClose(output_vector, target_vector, message=
                         "Network.predict error.")
        input_vector = [5, 2, -1]
        target_vector = [1.6164330657508448e-06, 0.0095407829940506415,
                         0.42283954465081319]
        output_vector = nn.predict(input_vector)
        self.assertClose(output_vector, target_vector, message=
                         "Network.predict error.")
    def test_predict_wide(self):
        nn = NN.Network(4, 2, [20], weight_scale=10, random_seed=91)
        input_vector = [-1, 0, 1, 2]
        target_vector = [0.88446717331877323, 0.99999999999999911]
        output_vector = nn.predict(input_vector)
        self.assertClose(output_vector, target_vector, message=
                         "Network.predict error.")
        input_vector = [-5, 0, -1, -1.5]
        target_vector = [1.0, 9.4855870942287332e-14]
        output_vector = nn.predict(input_vector)
        self.assertClose(output_vector, target_vector, message=
                         "Network.predict error.")
    def test_predict_deep(self):
        nn = NN.Network(1, 1, [2,3,4,5,4,3,2], weight_scale=10, random_seed=22)
        input_vector = [5.5]
        target_vector = [0.079550580569749604]
        output_vector = nn.predict(input_vector)
        self.assertClose(output_vector, target_vector, message=
                         "Network.predict error.")
        input_vector = [-5.0]
        target_vector = [0.079550580570209389]
        output_vector = nn.predict(input_vector)
        self.assertClose(output_vector, target_vector, message=
                         "Network.predict error.")

    def test_backpropagation_small(self):
        nn = NN.Network(3, 3, [3], weight_scale=.1, random_seed=74,
                        learning_rate=10)
        input_vector = [-1, 0, 1]
        nn.predict(input_vector)
        target_vector = [0., .5, 1.]
        nn.backpropagation(target_vector)
        weights = [[e.weight for e in n.out_edges] for n in nn.layers[0]]
        expected_weights = \
                [[0.036319633959432579, -0.11290500750462876,
                    -0.035007958284649393],
                 [0.085253228862123998, 0.073753705059175473,
                    -0.059679883330276906],
                 [0.11988016798353364, 0.1754042988325476,
                    -0.068349530989391408]]
        self.assertClose(weights, expected_weights, message=
                         "Network.backpropagation error.")
        input_vector = [5, 2, -1]
        nn.predict(input_vector)
        target_vector = [.9, .5, .1]
        nn.backpropagation(target_vector)
        weights = [[e.weight for e in n.out_edges] for n in nn.layers[0]]
        expected_weights = \
                [[-1.189984620537202, -1.4565500208831874,
                    -1.0525173157157277],
                 [-0.40526847293652979, -0.46370430029224807,
                     -0.46668362630270821],
                 [0.36514101888286055, 0.44413330150825936,
                     0.13515234049682423]]
        self.assertClose(weights, expected_weights, message=
                         "Network.backpropagation error.")
    def test_backpropagation_wide(self):
        nn = NN.Network(2, 4, [20], weight_scale=.1, random_seed=91,
                        learning_rate=10)
        input_vector = [-1, 0]
        nn.predict(input_vector)
        target_vector = [0, 1, 1, 0]
        nn.backpropagation(target_vector)
        weights = [[e.weight for e in n.out_edges] for n in nn.layers[0]]
        expected_weights = \
                [[-0.071492903626287255, -0.05816238760199402,
                  -0.03534024709141706, -0.0074214687423239528,
                  0.18498969560664008, -0.0961411450078892,
                  0.18063728584818162, 0.181133023184328,
                  0.0042128985429375852, 0.12931848600464421,
                  -0.12589355751686468, -0.24000775940669486,
                  0.023047766613129607, 0.16948680314228165,
                  0.14792772797407688, -0.027019939341866139,
                  0.024260766063869101, -0.055284070416947079,
                  -0.15507955962683462, -0.0016508518646832972],
                [-0.066477562575821533, 0.057844215254984593,
                  0.21173782908237093, -0.044639434521677783,
                  -0.066693906489248625, 0.048079724931287253,
                  0.19849801065676126, 0.039190893552514122,
                  0.23982028022526714, 0.24173602732584878,
                  -0.161411983056928, -0.021642658107796246,
                  0.16636321183995761, -0.012201627077841688,
                  0.1398420657053959, -0.063836467538069333,
                  -0.079995595017062604, 0.097931238253741282,
                  -0.097706732097435287, 0.052231952479944901]]
        self.assertClose(weights, expected_weights, message=
                         "Network.backpropagation error.")
        input_vector = [-5, 5]
        nn.predict(input_vector)
        target_vector = [0.1, 0.3, 0.5, 0.7]
        nn.backpropagation(target_vector)
        weights = [[e.weight for e in n.out_edges] for n in nn.layers[0]]
        expected_weights = \
                [[-0.063564105054976353,  -0.051852192557495742,
                  -0.030155824899281692,  -0.00041161932703303629,
                  0.18935121236082944,  -0.089404326356703048,
                  0.18544502265936483,  0.1875767624069741,
                  0.0096145523998172316,  0.13496652541688064,
                  -0.11898914074433696,  -0.23343026950553339,
                  0.029923943460375007,  0.17368059813176501,
                  0.15461536997364966,  -0.018118009116766205,
                  0.030974150401697258,  -0.048381843815970889,
                  -0.14634132674254666,  0.0051102628153846131],
                [-0.074406361147132435,  0.051534020210486316,
                  0.20655340689023557,  -0.051649283936968701,
                  -0.071055423243437985,  0.041342906280101101,
                  0.19369027384557805,  0.032747154329868036,
                  0.23441862636838748,  0.23608798791361235,
                  -0.1683163998294557,  -0.02822014800895771,
                  0.15948703499271222,  -0.016395422067325041,
                  0.13315442370582312,  -0.07273839776316926,
                  -0.086708979354890761,  0.091029011652765085,
                  -0.10644496498172325,  0.045470837799876991]]
        self.assertClose(weights, expected_weights, message=
                         "Network.backpropagation error.")
    def test_backpropagation_deep(self):
        nn = NN.Network(1, 1, [2,3,4,5,4,3,2], weight_scale=.1, random_seed=22,
                        learning_rate=10.)
        input_vector = [0.5]
        nn.predict(input_vector)
        target_vector = [1.]
        nn.backpropagation(target_vector)
        weights = [[e.weight for e in n.out_edges] for n in nn.layers[0]]
        expected_weights = [[-0.0091949919644617774, -0.14633506539676461]]
        self.assertClose(weights, expected_weights, rtol=1e-10, message=
                         "Network.backpropagation error.")
        input_vector = [-1.5]
        nn.predict(input_vector)
        target_vector = [0.]
        nn.backpropagation(target_vector)
        weights = [[e.weight for e in n.out_edges] for n in nn.layers[0]]
        expected_weights = [[-0.0091949923151859146, -0.14633506408885485]]
        self.assertClose(weights, expected_weights, rtol=1e-10, message=
                         "Network.backpropagation error.")


if __name__ == "__main__":
    unittest.main()
