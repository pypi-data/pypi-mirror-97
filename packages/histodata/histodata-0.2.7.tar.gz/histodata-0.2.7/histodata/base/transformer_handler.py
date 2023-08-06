from typing import Callable
from typing import Optional as O
from typing import Sequence
from typing import Union as U

from ..helper import helper
from . import transformer_adapters


def __set_values_to_input_dictionary__(dictionary, values):
    input_dic = {}
    for k in dictionary:
        input_dic[k] = values[dictionary[k]]
    return input_dic


def __update_output_dictionary_to_values__(dictionary, values, output_values):
    for k_result, k_dictionary in zip(output_values, dictionary):
        values[dictionary[k_dictionary]] = output_values[k_result]
    return values


class TransformerHandler:
    def __init__(
        self,
        transfs: O[U[Callable, Sequence[Callable]]] = None,
        access_orders: O[Sequence[Sequence[str]]] = None,
        is_callable_with_batches: O[Sequence[bool]] = None,
        seed: int = None,
    ):
        # convert or create list of pre_transformation_adapters
        self.transfs = helper.create_list_from_variable(transfs)

        # create a new access_orders list
        if access_orders is not None:
            if len(self.transfs) != len(access_orders):
                assert AssertionError(
                    "The list of transformers and the list of access_order must be have "
                    + "the same length."
                )
            self.access_orders = access_orders
            for idx, v in enumerate(self.access_orders):
                self.access_orders[idx] = helper.create_list_from_variable(v)
        else:
            self.access_orders = [[] for _ in self.transfs]

        # create a new is_callable_with_batches list
        if is_callable_with_batches is not None:
            if len(self.transfs) != len(is_callable_with_batches):
                assert AssertionError(
                    "The list of transformers and the list of is_callable_with_batches "
                    + "must be have the same length."
                )
            self.is_callable_with_batches = is_callable_with_batches
        else:
            self.is_callable_with_batches = [False for _ in self.transfs]

        self.seed = seed

    def append(self, trans, access_order=None, is_callable_with_batches=False):
        self.transfs.append(trans)
        if isinstance(access_order, str):
            access_order = [access_order]
        self.access_orders.append(access_order)
        if issubclass(type(trans), transformer_adapters.TransformerAdapter):
            self.is_callable_with_batches.append(trans.is_callable_with_batches)
        else:
            self.is_callable_with_batches.append(is_callable_with_batches)

    def replace(self, trans, access_order=None, is_callable_with_batches=False, index=-1):
        self.transfs[index] = trans
        if isinstance(access_order, str):
            access_order = [access_order]
        self.access_orders[index] = access_order
        if issubclass(type(trans), transformer_adapters.TransformerAdapter):
            self.is_callable_with_batches[index] = trans.is_callable_with_batches
        else:
            self.is_callable_with_batches[index] = is_callable_with_batches

    def __call_single_transform_with_dict__(
        self, item_or_batch, hashes, transf, dictionary, batch_callable
    ):
        is_batch = isinstance(hashes, list)

        if is_batch is False:
            if self.seed is not None:
                helper.set_random_seed_with_int(int(self.seed + hashes))
            input_dic = __set_values_to_input_dictionary__(dictionary, item_or_batch)
            result = transf(**input_dic)
            return __update_output_dictionary_to_values__(dictionary, item_or_batch, result)
        elif batch_callable and self.seed is None:
            input_dic = __set_values_to_input_dictionary__(dictionary, item_or_batch)
            result = transf(**input_dic)
            item_or_batch.update(result)
            return item_or_batch
        else:
            """
            result = {}
            for i in range(len(item_or_batch[list(item_or_batch)[0]])):
                if self.seed is not None:
                    helper.set_random_seed_with_int(int(self.seed + hashes[j]))
                element
                input_dic = __set_values_to_input_dictionary__(dictionary, item_or_batch)
                result = transf(**input_dic)
                item_or_batch.update(result)
            """
            raise NotImplementedError()

    def __call_single_transform_with_callable__(
        self, item_or_batch, hashes, transf, order, batch_callable
    ):
        is_batch = isinstance(hashes, list)

        if order is None or order == [] or order[0] is None or order[0] == "":
            order = list(item_or_batch)

        tmp_saved_seed_state = helper.get_random_seed()

        for i, name in enumerate(order):

            element = item_or_batch.pop(name)

            if is_batch is False:
                if self.seed is not None:
                    helper.set_random_seed_with_int(int(self.seed + hashes))
                result = transf(element)
            elif batch_callable and self.seed is None:
                result = transf(element)
            else:
                result = {}
                for j, item in enumerate(element):
                    if self.seed is not None:
                        helper.set_random_seed_with_int(int(self.seed + hashes[j]))

                    result_item = transf(item)

                    if isinstance(result_item, dict):
                        if j == 0:
                            for k in result_item:
                                result[name + "_" + k] = [result_item[k]]
                        else:
                            for k in result_item:
                                result[name + "_" + k].append(result_item[k])
                    else:
                        if j == 0:
                            result[name] = [result_item]
                        else:
                            result[name].append(result_item)

            if isinstance(result, dict):
                for k in result:
                    if k.startswith(name):
                        item_or_batch[k] = result[k]
                    else:
                        item_or_batch[name + "_" + k] = result[k]
            else:
                item_or_batch[name] = result

            # use the same seed for each data that contains to the same image.
            if i < len(order) - 1:
                helper.set_random_seed(*tmp_saved_seed_state)

        return item_or_batch

    def __call__(self, item_or_batch, hashes):

        if self.seed is not None:
            saved_seed_state = helper.get_random_seed()

        for (transf, order, batch_callable) in zip(
            self.transfs, self.access_orders, self.is_callable_with_batches
        ):
            if isinstance(order, dict):
                item_or_batch = self.__call_single_transform_with_dict__(
                    item_or_batch, hashes, transf, order, batch_callable
                )
            else:
                item_or_batch = self.__call_single_transform_with_callable__(
                    item_or_batch, hashes, transf, order, batch_callable
                )

        if self.seed is not None:
            helper.set_random_seed(*saved_seed_state)

        return item_or_batch

    def __len__(self):
        return len(self.transfs)

    def __call_with_prints__(self, item_or_batch, hashes):

        if self.seed is not None:
            saved_seed_state = helper.get_random_seed()

        index = 0
        for (transf, order, batch_callable) in zip(
            self.transfs, self.access_orders, self.is_callable_with_batches
        ):
            print(index, type(self.transfs))
            print("All Input-keys:", list(item_or_batch))
            print("Access Order", self.access_orders)
            index += 1

            if isinstance(order, dict):
                item_or_batch = self.__call_single_transform_with_dict__(
                    item_or_batch, hashes, transf, order, batch_callable
                )
            else:
                item_or_batch = self.__call_single_transform_with_callable__(
                    item_or_batch, hashes, transf, order, batch_callable
                )
            print("All Output-keys:", list(item_or_batch))
            print()

        if self.seed is not None:
            helper.set_random_seed(*saved_seed_state)

        return item_or_batch
