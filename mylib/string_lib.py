
class str_list_ops:

    def common_elements(list_a, list_b):
        a_set = set(list_a)
        b_set = set(list_b)
            
        # check length
        if len(a_set.intersection(b_set)) > 0:
            return list(a_set.intersection(b_set)) 
        else:
            return []

    def intersection_over_union(list1, list2):
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(set(list1)) + len(set(list2))) - intersection
        
        return float(intersection) / union


