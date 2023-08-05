import numpy as np

import mondobrain as mb

try:
    from indigo.camp import Tent
except Exception:
    raise Exception(
        "NLP tools have not been installed. Try running "
        "`pip install git+https://bitbucket.org/mondobrain/indigo@master#egg=indigo`"
    )


class MondoBot(object):
    """
    builds an object to ask a natural language question/demand
    and get a natural language answer back
    """

    def __init__(self, frame, message=None):
        self.solver = mb.Solver()

        self.frame = frame.copy()
        self.frame.columns = self.frame.columns.str.lower()
        self.message = message
        self.tent = Tent(dataset=self.frame, question=message)

        self._operation_dict = {
            "min": "minimized",
            "max": "maximized",
        }

    def __repr__(self):
        _repr = list()

        _repr.append(str(self.__class__))
        for feat in self.tent.stakes["features"]:

            explorable = outcome = constraint = "N/A"
            if "entities" in self.tent.stakes:
                explorable, outcome, constraint = "No", "No", "None"
                if feat["key"].lower() in (
                    expl.lower() for expl in self.tent.stakes["entities"]["explorable"]
                ):
                    explorable = "Yes"
                if (
                    feat["key"].lower()
                    == self.tent.stakes["entities"]["outcome"].lower()
                ):
                    if (
                        self.tent.stakes["entities"]["operation"]["type"]
                        == "continuous"
                    ):
                        outcome = f"Yes; {self._operation_dict[self.tent.stakes['entities']['operation']['value']]}"  # NOQA E501
                    else:
                        outcome = f"Yes; {feat['key']} = {self.tent.stakes['entities']['operation']['value']}"  # NOQA E501
                for const in self.tent.stakes["entities"]["constraints"]:
                    if feat["key"].lower() == const["feature"].lower():
                        constraint = " ".join(const.values())

            if feat["type"] == "continuous":
                _repr.append(
                    f"variable: {feat['key']}\n"
                    f"\t-type: {feat['type']}\n"
                    f"\t-range: {feat['range'][0]} to {feat['range'][1]}\n"
                    f"\t-explorable: {explorable}\n"
                    f"\t-outcome: {outcome}\n"
                    f"\t-constraint: {constraint}\n"
                )
            else:
                _repr.append(
                    f"variable: {feat['key']}\n"
                    f"\t-type: {feat['type']}\n"
                    f"\t-modalities: {', '.join(tuple(feat['modalities'][i] for i in range(5) if i < len(feat['modalities'])))}{'...' if len(feat['modalities']) > 5 else ''}\n"  # NOQA E501
                    f"\t-explorable: {explorable}\n"
                    f"\t-outcome: {outcome}\n"
                    f"\t-constraint: {constraint}\n"
                )

        return "\n".join(_repr)

    def _distinguish_discrete(self, rule_values):
        if isinstance(rule_values, str):
            return rule_values
        else:
            return f"between {rule_values['lo']} and {rule_values['hi']}"

    def _process_constraint(self, col, constraint, constraint_class=None):
        constraints = constraint.split(" ")
        if "=" in constraints:
            return self.frame[col] == constraint_class
        elif ">" in constraints:
            bound = float(constraints[1])
            return self.frame[col] > bound
        elif "<" in constraints:
            bound = float(constraints[1])
            return self.frame[col] < bound
        elif ">=" in constraints:
            bound = float(constraints[1])
            return self.frame[col] >= bound
        elif "<=" in constraints:
            bound = float(constraints[1])
            return self.frame[col] <= bound
        elif "between" in constraints:
            low, high = float(constraints[1]), float(constraints[3])
            return (self.frame[col] > low) & (self.frame[col] < high)
        else:
            return None

    def _verbalize(self, entities, rule):
        discrete_outcome = entities["operation"]["type"] == "discrete"
        if discrete_outcome:
            outcome_statement = (
                f"most significant with respect to \"{entities['operation']['value']}\""
            )
        else:
            outcome_statement = self._operation_dict[entities["operation"]["value"]]
        answer = f"\"{entities['outcome']}\" is {outcome_statement} when:\n"
        for column, result in rule.items():
            between = self._distinguish_discrete(result)
            answer += f'\t- "{column}" is {between}\n'
        if entities["constraints"]:
            answer += "\nconstraints applied:\n"
            for constraint in entities["constraints"]:
                answer += f"- \"{' '.join(constraint.values())}\"\n"

        return answer

    def ask(self, message=None):

        if message is None:
            message = self.message

        self.tent.pitch(question=message)
        entities = self.tent.stakes["entities"]
        self._repr = dict()

        mask = np.ones(self.frame.shape[0], dtype=bool)
        if entities["constraints"]:
            for constraint in entities["constraints"]:
                if "class" not in constraint:
                    col, equality = constraint["feature"], constraint["constraint"]
                    mask = np.bitwise_and(
                        mask, self._process_constraint(col.lower(), equality)
                    )
                else:
                    col, equality, constraint_class = (
                        constraint["feature"],
                        constraint["constraint"],
                        constraint["class"],
                    )
                    mask = np.bitwise_and(
                        mask,
                        self._process_constraint(
                            col.lower(), equality, constraint_class
                        ),
                    )

        mb_X = mb.MondoDataFrame(
            self.frame.loc[mask, [col.lower() for col in entities["explorable"]]]
        )
        mb_y = mb.MondoSeries(
            self.frame.loc[mask, entities["outcome"].lower()], name=entities["outcome"]
        )
        mb_y.target_class = entities["operation"]["value"]

        self.solver.fit(mb_X, mb_y)

        print(self._verbalize(entities=entities, rule=self.solver.rule))
