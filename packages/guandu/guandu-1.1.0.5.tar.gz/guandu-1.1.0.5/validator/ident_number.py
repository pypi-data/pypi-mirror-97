# encoding: utf-8
"""
    @Time   : 2021-03-09 15:40
    @Author : feikong
"""
import datetime


class ValidateIdentNumber(object):

    def __init__(self, ident_number: str):
        self.ident_number: str = ident_number
        self.year: int = int(self.ident_number[6:10])
        self.month: int = int(self.ident_number[10:12])
        self.day: int = int(self.ident_number[12:14])

    def check_is_leap_year(self) -> bool:
        """
        判断平闰年
        True 闰年
        False 平年
        """
        return True if (self.year % 400 == 0) or (self.year % 4 == 0 and self.year % 100 != 0) else False

    def check_ymd_is_valid(self) -> bool:
        """判断年月日是否合法"""
        # 年
        now_year = datetime.datetime.now().year
        if now_year - self.year > 120:
            return False
        # 月
        if self.month > 12:
            return False
        # 日
        if self.month in [1, 3, 5, 7, 8, 10, 12]:
            if self.day > 31:
                return False
        elif self.month in [4, 6, 9, 11]:
            if self.day > 30:
                return False
        else:
            if self.check_is_leap_year() and self.day > 29:
                return False
            if not self.check_is_leap_year() and self.day > 28:
                return False
        return True

    def check_last_num_is_valid(self) -> bool:
        """判断身份证最后一位校验位是否正确"""
        ident_num = self.ident_number[:-1]
        # 系数
        calc_coefficient = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 余数
        calc_remainder = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        count = map(lambda id_num, coefficient: int(id_num) * coefficient, ident_num, calc_coefficient)
        last_num = calc_remainder[sum(count) % 11]
        if self.ident_number[-1].upper() != last_num:
            return False
        return True

    def validate_id_number(self) -> bool:
        # 只校验18位的身份证
        if len(self.ident_number) != 18:
            return False
        if not self.check_ymd_is_valid():
            return False
        if not self.check_last_num_is_valid():
            return False
        return True


def validate_id_number(id_num: str) -> bool:
    return ValidateIdentNumber(id_num).validate_id_number()


if __name__ == '__main__':
    print(validate_id_number("421182192204075511"))
