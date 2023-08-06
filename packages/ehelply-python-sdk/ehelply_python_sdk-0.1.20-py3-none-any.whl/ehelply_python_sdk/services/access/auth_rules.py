from __future__ import annotations
from typing import List, Tuple, Callable
from ehelply_python_sdk.services.access.sdk import AuthModel


class AuthException(Exception):
    pass


class AuthRule:
    """
    Provides a nice interface into developing authorization rules for endpoints
    """

    # Global config of whether to exception if unauthorized. Useful for development
    exception_if_unauthorized: bool = True

    # The exception to throw when auth fails
    exception_to_throw: Exception = AuthException

    # Global config of whether to override auth rules. Essentially, bypass authorization. Useful for development
    override: bool = False

    def __init__(
            self,
            auth_model: AuthModel,
            *rules,
            exception_if_unauthorized: bool = None,
            exception_to_throw: Exception = None,
            override: bool = None,
            execute: bool = False
    ):
        if exception_if_unauthorized is None:
            exception_if_unauthorized = AuthRule.exception_if_unauthorized
        self.local_exception_if_unauthorized: bool = exception_if_unauthorized

        if exception_to_throw is None:
            exception_to_throw = AuthRule.exception_to_throw
        self.local_exception_to_throw: Exception = exception_to_throw

        if override is None:
            override = AuthRule.override
        self.local_override: bool = override

        self.rules: List[AuthRule] = list(rules)

        self.handlers: List[Tuple[Callable, dict]] = []

        self.auth_model: AuthModel = auth_model

        if execute:
            self.verify()

    def verify(self) -> bool:
        """
        Verifies that each changed rule passes using an AND logical operation.

        If rules were passed in, it will also verify that those pass successfully. The passed in rules become a logical OR

        Returns:

        """
        rules_passed: bool = False
        for rule in self.rules:
            try:
                result: bool = rule.verify()
                if result:
                    rules_passed = True
                    break
            except:
                pass

        if not rules_passed and len(self.rules) != 0:
            if self.local_exception_if_unauthorized:
                raise self.local_exception_to_throw
            else:
                return False

        for handler in self.handlers:
            try:
                result: bool = handler[0](**handler[1])
                if not result:
                    if self.local_exception_if_unauthorized:
                        raise self.local_exception_to_throw
                    else:
                        return False
            except:
                if self.local_exception_if_unauthorized:
                    raise self.local_exception_to_throw
                else:
                    return False

        return True

    def __handler_entity_identifier_eq(self, entity_identifier: str) -> bool:
        return self.auth_model.entity_identifier == entity_identifier

    def entity_identifier_eq(self, entity_identifier: str):
        self.handlers.append((
            self.__handler_entity_identifier_eq,
            {
                "entity_identifier": entity_identifier
            }
        ))

    def __handler_entity_identifier_neq(self, entity_identifier: str) -> bool:
        return self.auth_model.entity_identifier != entity_identifier

    def entity_identifier_neq(self, entity_identifier: str):
        self.handlers.append((
            self.__handler_entity_identifier_neq,
            {
                "entity_identifier": entity_identifier
            }
        ))

    def __handler_entity_has_node_on_target(self, node: str, target_identifier: str, partition: str) -> bool:
        return self.auth_model.access_sdk.is_allowed(
            auth_model=self.auth_model,
            target_identifier=target_identifier,
            node=node,
            partition=partition
        )

    def entity_has_node_on_target(self, node: str, target_identifier: str, partition: str = None) -> AuthRule:
        self.handlers.append((
            self.__handler_entity_has_node_on_target,
            {
                "node": node,
                "target_identifier": target_identifier,
                "partition": partition
            }
        ))
        return self

    def __handler_has_entity(self) -> bool:
        return self.auth_model.entity_identifier is not None

    def has_entity(self) -> AuthRule:
        self.handlers.append((
            self.__handler_has_entity,
            {}
        ))
        return self

    def __handler_has_participant(self) -> bool:
        return self.auth_model.active_participant_uuid is not None

    def has_participant(self) -> AuthRule:
        self.handlers.append((
            self.__handler_has_participant,
            {}
        ))
        return self

    def __handler_participant_has_node_on_target(self, node: str, target_identifier: str, partition: str) -> bool:
        temp_model: AuthModel = AuthModel(
            access_sdk=self.auth_model.access_sdk,
            active_participant_uuid=self.auth_model.active_participant_uuid,
            entity_identifier=self.auth_model.active_participant_uuid,
            project_uuid=self.auth_model.project_uuid,
            access_token=self.auth_model.access_token,
            secret_token=self.auth_model.secret_token,
            claims=self.auth_model.claims,
        )

        return self.auth_model.access_sdk.is_allowed(
            auth_model=temp_model,
            target_identifier=target_identifier,
            node=node,
            partition=partition
        )

    def participant_has_node_on_target(self, node: str, target_identifier: str, partition: str = None) -> AuthRule:
        self.handlers.append((
            self.__handler_participant_has_node_on_target,
            {
                "node": node,
                "target_identifier": target_identifier,
                "partition": partition
            }
        ))
        return self

    def __handler_participant_below_limit(self) -> bool:
        return True

    def participant_below_limit(self, limit: str) -> AuthRule:
        self.handlers.append((
            self.__handler_participant_below_limit,
            {
                "limit": limit
            }
        ))
        return self

    def __handler_customentity_has_node_on_target(
            self,
            node: str,
            target_identifier: str,
            partition: str,
            entity_identifier: str
    ) -> bool:
        temp_model: AuthModel = AuthModel(
            access_sdk=self.auth_model.access_sdk,
            active_participant_uuid=self.auth_model.active_participant_uuid,
            entity_identifier=entity_identifier,
            project_uuid=self.auth_model.project_uuid,
            access_token=self.auth_model.access_token,
            secret_token=self.auth_model.secret_token,
            claims=self.auth_model.claims,
        )

        return self.auth_model.access_sdk.is_allowed(
            auth_model=temp_model,
            target_identifier=target_identifier,
            node=node,
            partition=partition
        )

    def customentity_has_node_on_target(
            self,
            node: str,
            target_identifier: str,
            partition: str,
            entity_identifier: str
    ) -> AuthRule:
        self.handlers.append((
            self.__handler_customentity_has_node_on_target,
            {
                "node": node,
                "target_identifier": target_identifier,
                "partition": partition,
                "entity_identifier": entity_identifier
            }
        ))
        return self
    
    def __handler_project_uuid_eq(self, project_uuid: str) -> bool:
        return self.auth_model.project_uuid == project_uuid

    def project_uuid_eq(self, project_uuid: str):
        self.handlers.append((
            self.__handler_project_uuid_eq,
            {
                "project_uuid": project_uuid
            }
        ))

    def __handler_project_uuid_neq(self, project_uuid: str) -> bool:
        return self.auth_model.project_uuid != project_uuid

    def project_uuid_neq(self, project_uuid: str):
        self.handlers.append((
            self.__handler_project_uuid_neq,
            {
                "project_uuid": project_uuid
            }
        ))
