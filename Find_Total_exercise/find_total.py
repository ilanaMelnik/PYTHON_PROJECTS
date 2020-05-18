
"""
public class MovingTotal {
    /**
     * Adds/appends list of integers at the end of internal list.
     */
    public void append(int[] list) {
        throw new UnsupportedOperationException("Waiting to be implemented.");
    }

    /**
     * Returns boolean representing if any three consecutive integers in the
     * internal list have given total.
     */
    public boolean contains(int total) {
        throw new UnsupportedOperationException("Waiting to be implemented.");
    }

    public static void main(String[] args) {
        MovingTotal movingTotal = new MovingTotal();

        movingTotal.append(new int[] { 1, 2, 3 });

        System.out.println(movingTotal.contains(6));
        System.out.println(movingTotal.contains(9));

        movingTotal.append(new int[] { 4 });

        System.out.println(movingTotal.contains(6));
        System.out.println(movingTotal.contains(9));
    }
}
"""


class FindTotal:
    def __init__(self):
        self.cnt = 0
        self.nums_list = []
        self.my_totals_dict = {}
        self.amount_left = 2

    def add_new_total(self, new_total):
        self.my_totals_dict.update({new_total: 1})  # added <new_total, 1>, value 1 is meaningless

    def check_total_exists(self, new_total):

        # handle first time
        if len(self.my_totals_dict) == 0:
            return False
        else:
            # dict exist, search the dict keys
            for total in self.my_totals_dict.keys():
                if new_total == total:
                    return True
        return False

    def calc_total(self, third_num):
        print("we gonna make total of this triplet, {} and {} ".format(self.nums_list, third_num))
        total = 0
        for elem in self.nums_list:
            total += elem
        total += third_num
        return  total

    # Adds / appends list of integers at the end of internal list.
    def append(self, list_of_integers):
        print("new numbers are: {}, new total will be calculated if possible ".format(list_of_integers))

        # run over a given list, work with each number
        for num in list_of_integers:
            if self.cnt < self.amount_left:
                self.cnt += 1
                self.nums_list.append(num)

            # after each append check if you can calculate new total and check if such already exists in by dict
            elif self.cnt == self.amount_left:
                # reset the counter
                self.cnt = 0
                # calculate total
                total = self.calc_total(num) # 2 that already in the list plus current
                # add this total only if it does not exist
                if not self.check_total_exists(total):
                    self.add_new_total(total)

                # keep only two last elems
                self.nums_list[0] = self.nums_list[1]
                self.nums_list[1] = num

                # from this moment each new arrived elem will be checked against two last elems
                self.amount_left = 0


    # Returns boolean representing if any three consecutive integers in the internal list have given total.
    def contains(self, total):
        print("check if given total: {}, is existing ".format(total))
        if not self.check_total_exists(total):
            return False
        return True


if __name__ == "__main__":
    find_total = FindTotal()

    find_total.append([1])
    print(find_total.contains(6))
    find_total.append([2])
    print(find_total.contains(9))
    find_total.append([2])
    print(find_total.contains(5))
    find_total.append([1])
    print(find_total.contains(5))
    print(find_total.contains(7))
    find_total.append([1,1,1])
    print(find_total.contains(4))
    print(find_total.contains(3))

    # check if incoming is empty list
    find_total.append([])
    print(find_total.contains(4))



