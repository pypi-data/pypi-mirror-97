"""Gov module message types."""

from __future__ import annotations

import attr

from terra_sdk.core import AccAddress, Coins
from terra_sdk.core.msg import Msg

from .data import Content

__all__ = ["MsgSubmitProposal", "MsgDeposit", "MsgVote"]


@attr.s
class MsgSubmitProposal(Msg):
    """Submit the attached proposal with an initial deposit.

    Args:
        content (Content): type of proposal
        initial_deposit (Coins): initial deposit for proposal made by proposer
        proposer: proposal submitter
    """

    type = "gov/MsgSubmitProposal"
    """"""
    action = "submit_proposal"
    """"""

    content: Content = attr.ib()
    initial_deposit: Coins = attr.ib(converter=Coins)
    proposer: AccAddress = attr.ib()

    @classmethod
    def from_data(cls, data: dict) -> MsgSubmitProposal:
        from terra_sdk.util.parse_content import parse_content

        data = data["value"]
        content = parse_content(data["content"])
        return cls(
            content=content,
            initial_deposit=Coins.from_data(data["initial_deposit"]),
            proposer=data["proposer"],
        )


@attr.s
class MsgDeposit(Msg):
    """Deposit funds for an active deposit-stage proposal.

    Args:
        proposal_id: proposal number to deposit for
        depositor: account making deposit
        amount (Coins): amount to deposit
    """

    type = "gov/MsgDeposit"
    """"""
    action = "deposit"
    """"""

    proposal_id: int = attr.ib(converter=int)
    depositor: AccAddress = attr.ib()
    amount: Coins = attr.ib(converter=Coins)

    def to_data(self) -> dict:
        return {
            "type": self.type,
            "value": {
                "proposal_id": str(self.proposal_id),
                "depositor": self.depositor,
                "amount": self.amount.to_data(),
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgDeposit:
        data = data["value"]
        return cls(
            proposal_id=data["proposal_id"],
            depositor=data["depositor"],
            amount=Coins.from_data(data["amount"]),
        )


@attr.s
class MsgVote(Msg):
    """Vote for an active voting-stage proposal.

    Args:
        proposal_id: proposal to vote for
        voter: account casting vote
        option: vote option (must be one of: :data:`MsgVote.ABSTAIN`,
            :data:`MsgVote.YES`, :data:`MsgVote.NO`, or :data:`MsgVote.NO_WITH_VETO`,
    """

    type = "gov/MsgVote"
    """"""
    action = "vote"
    """"""

    EMPTY = "Empty"
    """Encodes an empty vote option."""

    YES = "Yes"
    """"""
    ABSTAIN = "Abstain"
    """"""
    NO = "No"
    """"""
    NO_WITH_VETO = "NoWithVeto"
    """"""

    proposal_id: int = attr.ib(converter=int)
    voter: AccAddress = attr.ib()
    option: str = attr.ib()

    @option.validator
    def _check_option(self, attribute, value):
        possible_options = [
            self.EMPTY,
            self.YES,
            self.ABSTAIN,
            self.NO,
            self.NO_WITH_VETO,
        ]
        if value not in possible_options:
            raise TypeError(
                f"incorrect value for option: {value}, must be one of: {possible_options}"
            )

    def to_data(self) -> dict:
        return {
            "type": self.type,
            "value": {
                "proposal_id": str(self.proposal_id),
                "voter": self.voter,
                "option": self.option,
            },
        }

    @classmethod
    def from_data(cls, data: dict) -> MsgVote:
        data = data["value"]
        return cls(
            proposal_id=data["proposal_id"],
            voter=data["voter"],
            option=data["option"],
        )
