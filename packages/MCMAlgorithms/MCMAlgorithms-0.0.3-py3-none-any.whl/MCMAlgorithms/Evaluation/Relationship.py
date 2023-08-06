import sys
sys.path.append('..')
import numpy as np
import scipy.optimize as optim
import scipy.stats as stats
import copy
from Regression import Simple


class GreyAnalysis:

    def __init__(self, rho=0.5, mode='average'):
        """
        The setting of gray analysis
        :param rho: recognition coefficient, with default as 0.5, positive float
        :param mode: the method of removing dimension, with default as 'average', string in ('first', 'average')
        """
        self.__rho = rho
        self.__mode = mode.lower() if mode.lower() in ('first', 'average') else 'average'

    def analyse(self, base, data):
        """
        Apply grey analysis
        :param base: base sequence, 1-D ndarray
        :param data: 2-D ndarray, sequences for relationship calculating, each column is a sequence, the length should be equal to base
        :return: 1-D ndarray, each element indicates the corresponding relationship between the sequence and the base sequence
        """
        # Initialization
        base = np.array(base).squeeze()
        data = np.array(data)
        assert len(base) == data.shape[0]
        standard = np.mean(data, 0) if self.__mode == 'average' else data[0, :]
        no_dimension_data = data / standard
        standard = np.mean(base) if self.__mode == 'average' else base[0]
        no_dimension_base = base / standard
        # Calculate the relationship
        delta = np.abs(no_dimension_base.reshape(-1, 1) - no_dimension_data)
        max_relationship = np.max(delta)
        min_relationship = np.min(delta)
        xis = (min_relationship + self.__rho * max_relationship) / (delta + self.__rho * max_relationship)
        relationship = np.mean(xis, 0)
        return relationship


class DataEnvelope:

    def analyse(self, inputs, outputs):
        """
        Apply DEA analysis
        :param inputs: input data, with each column as a kind of input and row as observation, 2-D ndarray or 2-D torch tensor
        :param outputs: output data, with each column as a kind of output and row as observation, 2-D ndarray or 2-D torch tensor
        :return: efficient of each observation
        """
        # Initialization
        inputs = np.array(inputs)
        outputs = np.array(outputs)
        object_num, inputs_num = inputs.shape
        outputs_num = outputs.shape[1]
        # Programming
        b = np.zeros((object_num, 1))
        A = np.hstack((-outputs, inputs))
        evaluation = np.zeros(object_num)
        for idx in range(object_num):
            c = np.hstack((outputs[idx, :], np.zeros((1, inputs_num)).squeeze()))
            aeq = np.hstack((np.zeros((1, outputs_num)).squeeze(), inputs[idx, :])).reshape(1, -1)
            beq = 1
            x = optim.linprog(-c, -A, b, aeq, beq, [(0, None)] * len(c))
            x = x.x
            evaluation[idx] = np.sum(x * c.squeeze())
        return evaluation


class TOPSIS:

    def __change(self, M, a, b, x):
        if x < a:
            return 1 - (a - x) / M
        elif x > b:
            return 1 - (x - b) / M
        else:
            return 1

    def analyse(self, data, attribute_type=None, attribute_weight=None):
        """
        Apply TOPSIS analysis
        :param data: ndarray with size (N, M), (N is the sample number, M is the attribute number)
        :param attribute_type: Dict, key: index of attribute, value: tuple(attribute type, best parameter)
               type 1: high-pripority attribute, best parameter shall be set None
               type 2: low-priority attribute, best parameter shall be set None
               type 3: middle-priority attribute, best parameter shall be the best value
               type 4: room-priority attribute, best paramter shall be the best room tuple (a, b)
               The default value of None means all attributes are high-priority attributes
        :param attribute_weight: 1-D ndarray, whose length shall be M, indicating the weight of each attribute
               The default value of None means the weight of all attribute are the same.
        :return: 1-D array whose length is N, each element is the TOPSIS score of the corresponding sample
        """
        # Initialization
        data = copy.deepcopy(data)
        attribute_num = data.shape[1]
        if attribute_type is None:
            attribute_type = dict.fromkeys(range(attribute_num))
            for num in range(attribute_num):
                attribute_type[num] = (1,)
        attribute_weight = np.ones(attribute_num)  / attribute_num if attribute_weight is None else attribute_weight
        # Change the attribute to type 1
        for idx in range(attribute_num):
            if attribute_type[idx][0] == 2:
                data[:, idx] = np.max(data[:, idx]) - data[:, idx]
            elif attribute_type[idx][0] == 3:
                best = attribute_type[idx][1]
                M = np.max(np.abs(data[:, idx] - best))
                data[:, idx] = 1 - np.abs(data[:, idx] - best) / M
            elif attribute_type[idx][0] == 4:
                (a, b) = attribute_type[idx][1]
                if a > b:
                    a, b = b, a
                if a == b:
                    best = a
                    M = np.max(np.abs(data[:, idx] - best))
                    data[:, idx] = 1 - np.abs(data[:, idx] - best) / M
                else:
                    M = np.max([a - np.min(data[:, idx]), np.max(data[:, idx]) - b])
                    data[:, idx] = np.array(list(map(lambda x: self.__change(M, a, b, x), data[:, idx])))
        # Standardization
        data = data / np.sqrt(np.sum(data ** 2, 0))
        # Calculate the score
        z_plus = np.max(data, 0)
        z_minus = np.min(data, 0)
        d_plus = np.sqrt(np.sum(attribute_weight * (z_plus - data) ** 2, 1))
        d_minus = np.sqrt(np.sum(attribute_weight * (z_minus - data) ** 2, 1))
        score = d_minus / (d_plus + d_minus)
        return score


class RSR:

    def __init__(self):
        self.__probit_threshold = np.array([0.0000, 1.9098, 2.1218, 2.2522, 2.3479, 2.4242, 2.4879, 2.5427,
                                            2.5911, 2.6344, 2.6737, 2.7096, 2.7429, 2.7738, 2.8027, 2.8299,
                                            2.8556, 2.8799, 2.9034, 2.9251, 2.9463, 2.9665, 2.9859, 3.0046,
                                            3.0226, 3.0400, 3.0569, 3.0732, 3.0890, 3.1043, 3.1192, 3.1337,
                                            3.1478, 3.1616, 3.1759, 3.1881, 3.2009, 3.2134, 3.2256, 3.2376,
                                            3.2493, 3.2608, 3.2721, 3.2831, 3.2940, 3.3046, 3.3151, 3.3253,
                                            3.3354, 3.3454, 3.3551, 3.3648, 3.3742, 3.3836, 3.3928, 3.4018,
                                            3.4107, 3.4195, 3.4282, 3.4268, 3.4452, 3.4536, 3.4618, 3.4699,
                                            3.4780, 3.4859, 3.4937, 3.5015, 3.5091, 3.5167, 3.5242, 3.5316,
                                            3.5389, 3.5462, 3.5534, 3.5606, 3.5675, 3.5745, 3.5813, 3.5882,
                                            3.5949, 3.6016, 3.6083, 3.6148, 3.6213, 3.6278, 3.6342, 3.6405,
                                            3.6468, 3.6531, 3.6592, 3.6654, 3.6715, 3.6775, 3.6835, 3.6894,
                                            3.6953, 3.7012, 3.7070, 3.7127, 3.7184, 3.7241, 3.7298, 3.7354,
                                            3.7409, 3.7464, 3.7519, 3.7547, 3.7625, 3.7681, 3.7735, 3.7788,
                                            3.7840, 3.7893, 3.7945, 3.7996, 3.8048, 3.8099, 3.8150, 3.8200,
                                            3.8250, 3.8300, 3.8350, 3.8399, 3.8448, 3.8497, 3.8545, 3.8593,
                                            3.8641, 3.8689, 3.8736, 3.8783, 3.8830, 3.8877, 3.8923, 3.8969,
                                            3.9015, 3.9061, 3.9107, 3.9152, 3.9197, 3.9242, 3.9268, 3.9331,
                                            3.9375, 3.9419, 3.9463, 3.9506, 3.9550, 3.9593, 3.9636, 3.9678,
                                            3.9721, 3.9763, 3.9806, 3.9848, 3.9890, 3.9931, 3.9973, 4.0014,
                                            4.0055, 4.0096, 4.0137, 4.0178, 4.0218, 4.0259, 4.0299, 4.0339,
                                            4.0379, 4.0419, 4.0458, 4.0498, 4.0537, 4.0576, 4.0615, 4.0654,
                                            4.0693, 4.0731, 4.0770, 4.0808, 4.0846, 4.0884, 4.0922, 4.0960,
                                            4.0998, 4.1035, 4.1073, 4.1110, 4.1147, 4.1184, 4.1221, 4.1258,
                                            4.1295, 4.1331, 4.1367, 4.1404, 4.1440, 4.1476, 4.1512, 4.1548,
                                            4.1584, 4.1619, 4.1655, 4.1690, 4.1726, 4.1761, 4.1796, 4.1831,
                                            4.1866, 4.1901, 4.1936, 4.1970, 4.2005, 4.2039, 4.2074, 4.2108,
                                            4.2142, 4.2176, 4.2210, 4.2244, 4.2278, 4.2312, 4.2345, 4.2379,
                                            4.2412, 4.2446, 4.2479, 4.2512, 4.2546, 4.2579, 4.2612, 4.2644,
                                            4.2677, 4.2710, 4.2743, 4.2775, 4.2808, 4.2840, 4.2872, 4.2905,
                                            4.2937, 4.2969, 4.3001, 4.3033, 4.3065, 4.3097, 4.3129, 4.3160,
                                            4.3192, 4.3224, 4.3255, 4.3287, 4.3318, 4.3349, 4.3380, 4.3412,
                                            4.3443, 4.3474, 4.3505, 4.3536, 4.3567, 4.3597, 4.3628, 4.3659,
                                            4.3689, 4.3720, 4.3750, 4.3781, 4.3811, 4.3842, 4.3872, 4.3908,
                                            4.3932, 4.3962, 4.3992, 4.4022, 4.4052, 4.4082, 4.4112, 4.4142,
                                            4.4172, 4.4201, 4.4231, 4.4260, 4.4290, 4.4319, 4.4349, 4.4378,
                                            4.4408, 4.4437, 4.4466, 4.4495, 4.4524, 4.4554, 4.4583, 4.4612,
                                            4.4641, 4.4670, 4.4698, 4.4727, 4.4756, 4.4785, 4.4813, 4.4842,
                                            4.4871, 4.4899, 4.4982, 4.4956, 4.4985, 4.5013, 4.5041, 4.5050,
                                            4.5098, 4.5129, 4.5155, 4.5183, 4.5211, 4.5239, 4.5267, 4.5295,
                                            4.5323, 4.5351, 4.5379, 4.5407, 4.5435, 4.5462, 4.5490, 4.5518,
                                            4.5546, 4.5573, 4.5601, 4.5628, 4.5656, 4.5684, 4.5711, 4.5739,
                                            4.5766, 4.5793, 4.5821, 4.5845, 4.5875, 4.5903, 4.5930, 4.5957,
                                            4.5984, 4.6011, 4.6039, 4.6066, 4.6093, 4.6120, 4.6147, 4.6174,
                                            4.6201, 4.6228, 4.6255, 4.6281, 4.6308, 4.6335, 4.6362, 4.6389,
                                            4.6415, 4.6442, 4.6469, 4.6495, 4.6522, 4.6549, 4.6575, 4.6602,
                                            4.6628, 4.6655, 4.6681, 4.6708, 4.6734, 4.6761, 4.6787, 4.6814,
                                            4.6840, 4.6866, 4.6893, 4.6919, 4.6945, 4.6971, 4.6992, 4.7024,
                                            4.7050, 4.7076, 4.7102, 4.7129, 4.7155, 4.7181, 4.7207, 4.7233,
                                            4.7259, 4.7285, 4.7311, 4.7337, 4.7363, 4.7389, 4.7415, 4.7441,
                                            4.7467, 4.7492, 4.7518, 4.7544, 4.7570, 4.7596, 4.7622, 4.7647,
                                            4.7673, 4.7699, 4.7725, 4.7750, 4.7776, 4.7802, 4.7827, 4.7853,
                                            4.7879, 4.7904, 4.7930, 4.7955, 4.7981, 4.8007, 4.8032, 4.8058,
                                            4.8083, 4.8109, 4.8134, 4.8160, 4.8185, 4.8211, 4.8236, 4.8262,
                                            4.8287, 4.8313, 4.8338, 4.8363, 4.8389, 4.8414, 4.8440, 4.8465,
                                            4.8490, 4.8516, 4.8541, 4.8566, 4.8592, 4.8617, 4.8642, 4.8668,
                                            4.8693, 4.8718, 4.8743, 4.8769, 4.8794, 4.8819, 4.8844, 4.8870,
                                            4.8895, 4.8920, 4.8945, 4.8970, 4.8995, 4.9021, 4.9046, 4.9071,
                                            4.9096, 4.9122, 4.9147, 4.9172, 4.9197, 4.9222, 4.9247, 4.9272,
                                            4.9298, 4.9323, 4.9358, 4.9373, 4.9398, 4.9423, 4.9448, 4.9473,
                                            4.9498, 4.9524, 4.9549, 4.9574, 4.9599, 4.9624, 4.9649, 4.9674,
                                            4.9699, 4.9724, 4.9749, 4.9774, 4.9799, 4.9825, 4.9850, 4.9875,
                                            4.9900, 4.9925, 4.9950, 4.9975, 5.0000, 5.0025, 5.0050, 5.0075,
                                            5.0100, 5.0125, 5.0150, 5.0175, 5.0201, 5.0226, 5.0251, 5.0276,
                                            5.0301, 5.0326, 5.0351, 5.0376, 5.0401, 5.0426, 5.0451, 5.0476,
                                            5.0502, 5.0527, 5.0552, 5.0577, 5.0602, 5.0627, 5.0652, 5.0677,
                                            5.0702, 5.0728, 5.0753, 5.0778, 5.0803, 5.0828, 5.0853, 5.0878,
                                            5.0904, 5.0929, 5.0954, 5.0979, 5.1004, 5.1030, 5.1055, 5.1080,
                                            5.1105, 5.1130, 5.1156, 5.1181, 5.1206, 5.1231, 5.1257, 5.1282,
                                            5.1307, 5.1332, 5.1358, 5.1383, 5.1408, 5.1434, 5.1459, 5.1484,
                                            5.1510, 5.1535, 5.1560, 5.1586, 5.1611, 5.1637, 5.1662, 5.1687,
                                            5.1713, 5.1738, 5.1764, 5.1789, 5.1815, 5.1840, 5.1866, 5.1891,
                                            5.1917, 5.1942, 5.1968, 5.1993, 5.2019, 5.2045, 5.2070, 5.2096,
                                            5.2121, 5.2147, 5.2173, 5.2198, 5.2224, 5.2250, 5.2275, 5.2301,
                                            5.2327, 5.2353, 5.2378, 5.2404, 5.2430, 5.2456, 5.2482, 5.2508,
                                            5.2533, 5.2559, 5.2585, 5.2611, 5.2627, 5.2663, 5.2689, 5.2715,
                                            5.2741, 5.2767, 5.2793, 5.2819, 5.2845, 5.2871, 5.2898, 5.2924,
                                            5.2950, 5.2976, 5.3002, 5.3029, 5.3055, 5.3081, 5.3107, 5.3134,
                                            5.3160, 5.3186, 5.3213, 5.3239, 5.3266, 5.3292, 5.3319, 5.3345,
                                            5.3372, 5.3398, 5.3425, 5.3451, 5.3478, 5.3505, 5.3531, 5.3558,
                                            5.3585, 5.3611, 5.3638, 5.3665, 5.3692, 5.3719, 5.3745, 5.3772,
                                            5.3799, 5.3826, 5.3853, 5.3880, 5.3907, 5.3934, 5.3961, 5.3989,
                                            5.4016, 5.4043, 5.4070, 5.4097, 5.4125, 5.4152, 5.4179, 5.4207,
                                            5.4234, 5.4261, 5.4289, 5.4310, 5.4344, 5.4372, 5.4399, 5.4427,
                                            5.4454, 5.4482, 5.4510, 5.4538, 5.4565, 5.4593, 5.4621, 5.4649,
                                            5.4677, 5.4705, 5.4733, 5.4761, 5.4689, 5.4817, 5.4845, 5.4874,
                                            5.4902, 5.4930, 5.4858, 5.4987, 5.5015, 5.5044, 5.5072, 5.5101,
                                            5.5129, 5.5158, 5.5187, 5.5215, 5.5244, 5.5273, 5.5302, 5.5330,
                                            5.5359, 5.5388, 5.5417, 5.5445, 5.5476, 5.5505, 5.5534, 5.5563,
                                            5.5592, 5.5622, 5.5651, 5.5681, 5.5710, 5.5740, 5.5769, 5.5799,
                                            5.5828, 5.5858, 5.5888, 5.5918, 5.5948, 5.5978, 5.6008, 5.6038,
                                            5.6068, 5.6098, 5.6128, 5.6158, 5.6189, 5.6219, 5.6250, 5.6280,
                                            5.6311, 5.6341, 5.6372, 5.6403, 5.6433, 5.6464, 5.6495, 5.6526,
                                            5.6557, 5.6588, 5.6620, 5.5651, 5.6682, 5.6713, 5.6745, 5.6776,
                                            5.6808, 5.6840, 5.6871, 5.6903, 5.6935, 5.6967, 5.6999, 5.7031,
                                            5.7063, 5.7095, 5.7128, 5.7160, 5.7192, 5.7225, 5.7257, 5.7290,
                                            5.7323, 5.7356, 5.7388, 5.7421, 5.7454, 5.7488, 5.7521, 5.7554,
                                            5.7588, 5.7621, 5.7655, 5.7688, 5.7722, 5.7756, 5.7790, 5.7824,
                                            5.7858, 5.7892, 5.7926, 5.7961, 5.7995, 5.8030, 5.8064, 5.8099,
                                            5.8134, 5.8169, 5.8204, 5.8239, 5.8274, 5.8310, 5.8345, 5.8331,
                                            5.8416, 5.8452, 5.8488, 5.8524, 5.8560, 5.8596, 5.8633, 5.8669,
                                            5.8705, 5.8742, 5.8779, 5.8816, 5.8853, 5.8890, 5.8927, 5.8965,
                                            5.9002, 5.9040, 5.9078, 5.9116, 5.9154, 5.9192, 5.9230, 5.9269,
                                            5.9307, 5.9346, 5.9385, 5.9424, 5.9463, 5.9502, 5.9542, 5.9581,
                                            5.9621, 5.9661, 5.9701, 5.9741, 5.9782, 5.9822, 5.9863, 5.9904,
                                            5.9945, 5.9985, 5.0027, 6.0069, 6.0110, 6.0152, 6.0194, 6.0237,
                                            6.0279, 6.0322, 6.0364, 6.0407, 6.0450, 6.0494, 6.0537, 6.0581,
                                            6.0625, 6.0669, 6.0714, 6.0758, 6.0803, 6.0848, 6.0893, 6.0929,
                                            6.0985, 6.1031, 6.1077, 6.1123, 6.1170, 6.1217, 6.1264, 6.1311,
                                            6.1359, 6.1407, 6.1455, 6.1503, 6.1552, 6.1601, 6.1650, 6.1700,
                                            6.1750, 6.1800, 6.1850, 6.1901, 6.1952, 6.2004, 6.2055, 6.2107,
                                            6.2160, 6.2212, 6.2265, 6.2319, 6.2372, 6.2426, 6.2431, 6.2536,
                                            6.2591, 6.2646, 6.2702, 6.2759, 6.2816, 6.2673, 6.2930, 6.2988,
                                            6.3047, 6.3106, 6.3165, 6.3225, 6.3285, 6.3346, 6.3408, 6.3469,
                                            6.3532, 6.3595, 6.3658, 6.3722, 6.3787, 6.3852, 6.3917, 6.3984,
                                            6.4051, 6.4118, 6.4187, 6.4255, 6.4325, 6.4395, 6.4466, 6.4538,
                                            6.4611, 6.4584, 6.5758, 6.4833, 6.4909, 6.4985, 6.5063, 6.5141,
                                            6.5220, 6.5301, 6.5328, 6.5484, 6.5548, 6.5632, 6.5718, 6.5805,
                                            6.5893, 6.5982, 6.6072, 6.6164, 6.6258, 6.6352, 6.6449, 6.6546,
                                            6.6646, 6.6747, 6.6849, 6.6954, 6.7050, 6.7169, 6.7279, 6.7392,
                                            6.7507, 6.7624, 6.7744, 6.7866, 6.7991, 6.8119, 6.8250, 6.8384,
                                            6.8522, 6.8663, 6.8808, 6.8957, 6.9110, 6.9268, 6.9431, 6.9600,
                                            6.9774, 6.9954, 7.0141, 7.0335, 7.0537, 7.0749, 7.0969, 7.1201,
                                            7.1444, 7.1701, 7.1973, 7.2262, 7.2571, 7.2904, 7.3263, 7.3656,
                                            7.4089, 7.4573, 7.5121, 7.5758, 7.6521, 7.7478, 7.8782, 8.0900])
        self.__regression_tool = Simple.Linear()


    def analyse(self, data, attribute_type=None, attribute_weight=None, threshold=None):
        """
        Apply RSR analysis
        :param data: ndarray with size (N, M), (N is the sample number, M is the attribute number)
        :param attribute_type: 1-D ndarray indicating attribute type, whose length shall be M
               type 0: high-priority attribute
               type 1: low-priority attribute
               The default value of None means all attributes are high-priority attributes
        :param attribute_weight: 1-D ndarray, whose length shall be M, indicating the weight of each attribute
                                 The default value of None means the weight of all attribute are the same.
        :param threshold: 1-D ndarray, the threshold of dividing percentage, with default as (0.25, 0.5, 0.75)
        :return:(RSR value of each sample: 1-D ndarray, level of each sample: 1-D ndarray, significance RSR-probit relationship)
        """
        # Initialize the default parameters
        sample_num, attribute_num = data.shape
        attribute_type = np.zeros(attribute_num) if attribute_type is None else attribute_type.squeeze()
        attribute_weight = np.ones(attribute_num) / attribute_num if attribute_weight is None else attribute_weight.squeeze()
        threshold = np.array([0.25, 0.5, 0.75]) if threshold is None else threshold.squeeze()
        # Calculate the rank
        rank = np.zeros_like(data)
        for attribute_idx in range(attribute_num):
            attribute_rank = stats.rankdata(data[:, attribute_idx])
            if attribute_type[attribute_idx]:
                attribute_rank = sample_num - attribute_rank + 1
            rank[:, attribute_idx] = attribute_rank
        # Calculate the RSR value and the order
        RSR_value = (np.sum(attribute_weight * rank, 1) / sample_num).squeeze()
        # Divide into several levels
        Rbar = np.unique(stats.rankdata(np.sort(RSR_value)))
        percentage = 100 * Rbar / sample_num
        percentage[-1] = 100 * (1 - 1 / (4 * sample_num))
        percentage = np.around(percentage, 1)
        percentage[percentage == 100] = 99.9  # avoid 100%
        # Get the probit of each RSR value
        integral_part = np.floor(percentage).astype(np.int)
        decimal_part = (10 * (percentage - integral_part)).astype(np.int)
        probit_idx = 10 * integral_part + decimal_part
        probit = self.__probit_threshold[probit_idx]
        # Get the relationship between RSR value and probit value
        _0, _1, _2, significance = self.__regression_tool.fit(probit.reshape(-1, 1), np.unique(RSR_value).reshape(-1, 1))
        # Transfer threshold probability to probit
        threshold = np.around(threshold, 3) * 100
        threshold[threshold == 100] = 99.9
        integral_part = np.floor(threshold).astype(np.int)
        decimal_part = (10 * (threshold - integral_part)).astype(np.int)
        threshold_probit_idx = 10 * integral_part + decimal_part
        threshold_probit = self.__probit_threshold[threshold_probit_idx].squeeze()
        # Map the threshold probit to the RSR value
        threshold_RSR_value = self.__regression_tool.predict(threshold_probit.reshape(-1, 1)).squeeze()
        # Leveling
        total_level_num = len(threshold_RSR_value) + 1
        level = np.zeros(sample_num, dtype=np.int)
        for sample_idx in range(sample_num):
            idx = np.argwhere(threshold_RSR_value > RSR_value[sample_idx])
            if len(idx):
                level[sample_idx] = idx[0, 0] + 1
            else: # the highest level
                level[sample_idx] = total_level_num
        return RSR_value, level, significance
