import pandas as pd
import attr
import typing
import math


@attr.s(auto_attribs=True)
class IowaRecord:
    """
    A Iowa Gambling task experimental data record.

    Args:
        pull: The deck pull number.
        deck: Which deck did we draw from.
        win_amount: The amount the user won
        loss_amount: The amount the user lost.
        hunch: Does the user have a hunch yet?
        sure: Is the user sure yet?
    """
    pull: int
    deck: int
    win_amount: int = attr.ib(converter=int)
    loss_amount: int = attr.ib(converter=int)
    hunch: bool = attr.ib(converter=bool)
    sure: bool = attr.ib(converter=bool)


class IowaData:
    """
    A simple class to encapsulate the trial by trial data stored during the Iowa experiment.
    """

    def __init__(self):
        self.data = []
        self.trial_idx = 0

    def add_trial(self,
                  deck: int, win_amount: int, loss_amount: int, hunch: bool = False, sure: bool = False):
        """
        Record a trial to the dataset.

        Args:
            deck: Which deck did we draw from.
            win_amount: The amount the user won
            loss_amount: The amount the user lost.
            hunch: Does the user have a hunch yet?
            sure: Is the user sure yet?

        Returns:
            None
        """
        self.data.append(IowaRecord(pull=self.trial_idx,
                                    deck=deck, win_amount=win_amount, loss_amount=loss_amount,
                                    hunch=hunch, sure=sure))
        self.trial_idx = self.trial_idx + 1

    @property
    def num_pulls(self):
        """
        Get the number of deck pulls recorded.

        Returns:
            The number of deck pulls we have recorded.
        """
        return self.trial_idx

    def to_csv(self, filename: str):
        """
        Write the experimental data to CSV.

        Args:
            filename: The name of the CSV file for output.

        Returns:
            None
        """
        df = pd.DataFrame([attr.asdict(d) for d in self.data])
        df.to_csv(filename, index=False)



