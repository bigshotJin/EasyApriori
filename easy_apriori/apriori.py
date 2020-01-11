import sys
from collections.abc import Iterable
from easy_logging.easylogging import EasyVerboseLogging

EVLobj = EasyVerboseLogging()
EVLobj.show_class_log_output_path()
logger = EVLobj.get_class_logger()
sys.setrecursionlimit(3000)  # 手动设置递归的最大深度


class Apriori(object):
    """
    编程的核心思想：
        只考虑集合与集合之间是否是子集关系-重视是否是子集-采用 issubset
        一概不考虑 元素和集合的属于关系-无视属于-不采用 in
    """

    def __init__(self, input_list=None):
        self.logger = logger  # 日志器
        self.data_set = None  # 数据集
        self.set_input(list_value=input_list)  # 载入数据集
        self.set_default_input()  # 载入数据集
        self._check_input()  # 检查数据集
        self.min_support = 0.9  # 默认最小支持度
        self.support_set = dict()
        self.result_list = []

    def set_input(self, list_value=None):
        self.data_set = list_value

    def set_min_support(self, min_support):
        self.min_support = min_support

    def set_default_input(self):
        if self.data_set is None:
            # self.data_set = [
            #     ['豆奶', '莴苣'],
            #     ['莴苣', '尿布', '葡萄酒', '甜菜'],
            #     ['豆奶', '尿布', '葡萄酒', '橙汁'],
            #     ['莴苣', '豆奶', '尿布', '葡萄酒'],
            #     ['莴苣', '豆奶', '尿布', '橙汁']
            # ]
            self.data_set = [
                ['1', '3', '9', '13', '23', '25', '34', '36', '38', '40', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '107', '113'],
                ['2', '3', '9', '14', '23', '26', '34', '36', '39', '40', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '108', '114'],
                ['2', '4', '9', '15', '23', '27', '34', '36', '39', '41', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '108', '115'],
                ['1', '3', '10', '15', '23', '25', '34', '36', '38', '41', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '107', '113'],
                ['2', '3', '9', '16', '24', '28', '34', '37', '39', '40', '53', '54', '59', '63', '67', '76', '85',
                 '86', '90', '94', '99', '109', '114'],
                ['2', '3', '10', '14', '23', '26', '34', '36', '39', '41', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '108', '114'],
                ['2', '4', '9', '15', '23', '26', '34', '36', '39', '42', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '108', '115'],
                ['2', '4', '10', '15', '23', '27', '34', '36', '39', '41', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '115'],
                ['1', '3', '10', '15', '23', '25', '34', '36', '38', '43', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '110', '114'],
                ['2', '4', '9', '14', '23', '26', '34', '36', '39', '42', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '107', '115'],
                ['2', '3', '10', '14', '23', '27', '34', '36', '39', '42', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '108', '114'],
                ['2', '3', '10', '14', '23', '26', '34', '36', '39', '41', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '107', '115'],
                ['2', '4', '9', '14', '23', '26', '34', '36', '39', '44', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '114'],
                ['1', '3', '10', '15', '23', '25', '34', '36', '38', '40', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '110', '113'],
                ['2', '3', '11', '13', '24', '28', '34', '37', '39', '41', '53', '54', '59', '64', '67', '76', '85',
                 '86', '90', '94', '98', '109', '114'],
                ['2', '5', '11', '16', '24', '28', '34', '36', '38', '40', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '111', '113'],
                ['2', '6', '11', '15', '24', '28', '34', '37', '39', '40', '53', '54', '59', '63', '67', '76', '85',
                 '86', '90', '94', '99', '109', '114'],
                ['1', '3', '9', '13', '23', '25', '34', '36', '38', '41', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '107', '114'],
                ['1', '3', '10', '15', '23', '25', '34', '36', '38', '41', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '113'],
                ['1', '3', '9', '13', '23', '25', '34', '36', '38', '40', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '113'],
                ['2', '4', '9', '14', '23', '26', '34', '36', '39', '40', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '115'],
                ['1', '3', '10', '13', '23', '25', '34', '36', '38', '41', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '110', '114'],
                ['2', '4', '10', '14', '23', '27', '34', '36', '39', '40', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '115'],
                ['2', '4', '10', '15', '23', '26', '34', '36', '39', '44', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '108', '115'],
                ['2', '4', '9', '15', '23', '27', '34', '36', '39', '42', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '107', '115'],
                ['1', '6', '9', '15', '23', '25', '34', '36', '38', '41', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '110', '114'],
                ['2', '3', '10', '14', '23', '26', '34', '36', '39', '41', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '108', '115'],
                ['2', '3', '10', '15', '23', '27', '34', '36', '39', '44', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '108', '115'],
                ['2', '6', '11', '13', '24', '28', '34', '36', '38', '40', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '111', '113'],
                ['2', '3', '9', '14', '23', '26', '34', '37', '38', '41', '53', '56', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '110', '116'],
                ['2', '4', '9', '14', '23', '27', '34', '36', '39', '42', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '108', '115'],
                ['1', '3', '10', '15', '23', '25', '34', '36', '38', '40', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '113'],
                ['2', '3', '10', '14', '23', '27', '34', '36', '39', '41', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '108', '115'],
                ['2', '3', '10', '13', '23', '27', '34', '36', '39', '43', '52', '57', '59', '65', '67', '76', '85',
                 '86', '90', '93', '99', '111', '117'],
                ['2', '4', '10', '14', '23', '27', '34', '36', '39', '41', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '115'],
                ['2', '3', '11', '14', '23', '27', '34', '37', '38', '44', '53', '56', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '110', '116'],
                ['2', '5', '11', '16', '24', '28', '34', '36', '38', '40', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '110', '113'],
                ['1', '3', '10', '13', '23', '25', '34', '36', '38', '44', '52', '54', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '107', '113'],
                ['2', '3', '11', '14', '23', '26', '34', '37', '38', '43', '53', '56', '59', '63', '67', '76', '85',
                 '86', '90', '93', '99', '110', '116'],
                ['2', '4', '9', '14', '23', '27', '34', '36', '39', '40', '52', '55', '59', '63', '67', '76', '85',
                 '86', '90', '93', '98', '107', '115']]  # 毒蘑菇数据 建议最小支持度为0.9
            self.logger.info(f'未给定输入,暂时载入了样例{self.data_set}')

    def _check_input(self):
        tidy_input = []
        if isinstance(self.data_set, Iterable):
            for _list_item in self.data_set:
                tidy_str_list = []
                if (isinstance(_list_item, Iterable)
                        and not isinstance(_list_item, str)):
                    for _item in _list_item:
                        tidy_str_list.append(str(_item))
                    tidy_str_list = list(set(tidy_str_list))
                else:
                    self.logger.error(f'{_list_item} 必须为非字符串的可迭代类型,'
                                      f'可迭代属性为{isinstance(_list_item, Iterable)},'
                                      f'字符串情况为{isinstance(_list_item, str)}')
                    continue
                tidy_str_list.sort()
                tidy_input.append(tidy_str_list)
        else:
            self.logger.error(f'{self.data_set} 是不可迭代的!')
        self.data_set = tidy_input

    @staticmethod
    def _create_element_set(data_set):
        element_set = set()  # 空集
        for transaction in data_set:
            for item in transaction:
                if not set(item).issubset(element_set):
                    element_set.add(item)
        return element_set

    @staticmethod
    def _get_subset(original_set, set_scale):
        ret = []
        if isinstance(original_set, set):
            if 0 <= set_scale <= len(original_set):
                sub_set = Apriori._get_subset_from_list(
                    input_list=list(original_set),
                    subset_scale=set_scale)
                for item in sub_set:
                    ret.append(set(item))
            else:
                raise RuntimeError(f'长度为{len(original_set)},'
                                   f'无法生成元素为{set_scale}个的子集')
        else:
            raise TypeError(f'{original_set}必须为set类型')
        return ret

    @staticmethod
    def _get_subset_from_list(input_list, subset_scale):
        """
        通过递归的方式进行子集计算，该方法非常危险，可能瞬间占用所有的内存
        """
        ret = []
        if subset_scale <= 0:
            return ret

        if subset_scale == 1:
            for item in input_list:
                ret.append([item])
            return ret
        else:
            for index in range(len(input_list) - 1):
                ret_recursion = Apriori._get_subset_from_list(input_list[index + 1:], subset_scale - 1)
                for item in ret_recursion:
                    item.append(input_list[index])
                ret.extend(ret_recursion)
        return ret

    @staticmethod
    def _scan_data_set(data_set, freq_k_set, min_support):
        """
        data_set = [['1','2'],['2','3']]  # 二维列表 最底层每个元素均为 str 类型
        freq_k_set = [{'橙汁', '甜菜'},
                     {'甜菜', '葡萄酒'},
                     {'甜菜', '莴苣'},
                     {'尿布', '甜菜'},
                     {'甜菜', '豆奶'},
                     {'橙汁', '葡萄酒'},
                     {'橙汁', '莴苣'},
                     {'尿布', '橙汁'},
                     {'橙汁', '豆奶'},
                     {'莴苣', '葡萄酒'},
                     {'尿布', '葡萄酒'},
                     {'葡萄酒', '豆奶'},
                     {'尿布', '莴苣'},
                     {'莴苣', '豆奶'},
                     {'尿布', '豆奶'}]
        """
        if 0 <= min_support <= 1:
            pass
        else:
            raise ValueError(f'min_support 应该属于 0~1 之间')

        result_cnt = dict()
        for tid in data_set:
            s_tid = set(tid)
            for freq_k_element in freq_k_set:
                if freq_k_element.issubset(s_tid):
                    # 　frozenset是能够被哈希化的,因此可以作为字典的键
                    key_name = frozenset(freq_k_element)
                    if key_name in result_cnt:
                        result_cnt[key_name] += 1
                    else:
                        result_cnt[key_name] = 1

        # 样本数据集的条数
        item_numbers = len(data_set)
        ret_list = []
        support_data = dict()
        for key_name in result_cnt:
            support_value = result_cnt[key_name] / item_numbers
            if support_value >= min_support:
                ret_list.append(set(key_name))
            support_data[key_name] = support_value
        return ret_list, support_data

    @staticmethod
    def _generate_k_set(set_list, k):
        """
        创建提升后的 频繁项集合
        set_list  = [{'1','2'},{'1','3'},{'2','3'},{'1','4'},{'2','4'}]
        k = 3

        Return
        ------
        [{'1', '2', '4'}, {'1', '2', '3'}]
        """
        if k <= 0:
            raise RuntimeError(f'k 不应该小于等于 0')
        if len(set_list) == 0:
            return []
        element_set = Apriori._create_element_set(set_list)
        k_element_set_list = Apriori._get_subset_from_list(list(element_set), k)
        ret = []
        for k_element_set in k_element_set_list:
            should_add_flag = True
            check_set_list = Apriori._get_subset_from_list(k_element_set, k - 1)
            for check_set in check_set_list:
                if set(check_set) not in set_list:
                    should_add_flag = False
                    break
            if should_add_flag:
                ret.append(set(k_element_set))
        return ret

    def auto_run(self):
        init_element_set_c1 = self._create_element_set(self.data_set)
        k = 1
        freq_k_set = Apriori._get_subset(init_element_set_c1, k)
        while True:
            ret_list, support_data = Apriori._scan_data_set(data_set=self.data_set,
                                                            freq_k_set=freq_k_set,
                                                            min_support=self.min_support)
            if len(ret_list) == 0:
                break
            else:
                self.result_list.extend(ret_list)
                self.support_set.update(support_data)
                k = k + 1
                freq_k_set = Apriori._generate_k_set(ret_list, k)

        return self.result_list, self.support_set


if __name__ == "__main__":
    obj = Apriori()
    obj.auto_run()
