# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.types import DomainDict

class ValidaEscolhaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_escolha_form"


    def validate_produto(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida a Opção do Produto"""

        op = slot_value.lower()
        if op == "camisa" or op == "calça" or op == "bermuda" or \
            op == "camisas" or op == "calças" or op == "bermudas":
            return {"produto": op}
        else:
            dispatcher.utter_message(FollowupAction("action_opcao_estranha_produto"))
            return {"produto": None}

    def validate_tamanho(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida o tamanho do Produto"""

        op = slot_value.lower()
        if op == "p" or op == "m" or op == "g":
            return {"tamanho": op}
        else:
            dispatcher.utter_message(FollowupAction("action_opcao_estranha_tamanho"))
            return {"tamanho": None}

    def validate_quantidade(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Valida a Quantidade do Produto"""
        try:
            all_entities = tracker.latest_message.get("entities",[])
            entities = [e for e in all_entities if e.get("entity") == "number"]
            entity = entities[0]
            quantia = entity.get("additional_info", {}).get("value")
            if not quantia:
                raise (TypeError)
        except(TypeError,AttributeError):
            dispatcher.utter_message(FollowupAction("action_opcao_estranha_tamanho"))
            return {"quantidade": None}
        return {"quantidade": quantia}

class ActionOla(Action):

    def name(self) -> Text:
        return "action_ola"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            text = ['Ola! Qual produto vai hoje']
            for texto in text:
                dispatcher.utter_message(text=texto)
            return []

class ActionAskProduto(Action):

    def name(self) -> Text:
        return "action_ask_produto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            text = ['Temos camisas, calças e bermudas. qual vai?']
            for texto in text:
                dispatcher.utter_message(texto)
            return []

class ActionAskTamanho(Action):

    def name(self) -> Text:
        return "action_ask_tamanho"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            text = ['Qual o tamanho']
            for texto in text:
                dispatcher.utter_message(texto)
            return []    

class ActionAskQuantidade(Action):

    def name(self) -> Text:
        return "action_ask_quantidade"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            text = ['Quantas Peças']
            for texto in text:
                dispatcher.utter_message(texto)
            return []


class ActionObjetivos(Action):

    def name(self) -> Text:
        return "action_objetivos"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            text = ['Eu sou um bot que atende seus desejos','Qual produto vai hoje']
            for texto in text:
                dispatcher.utter_message(texto)
            return []

class ActionOpcaoEstranhaProduto(Action):

    def name(self) -> Text:
        return "action_opcao_estranha_produto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            text = ['Parece que não tenho esse produto','Temos camisas, calças e bermudas']
            for texto in text:
                dispatcher.utter_message(texto)
            return []

class ActionOpcaoEstranhaTamanho(Action):

    def name(self) -> Text:
        return "action_opcao_estranha_tamanho"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            text = ['Preciso do tamanho da peça: p, m ou g. ']
            for texto in text:
                dispatcher.utter_message(texto)
            return []

class ActionOpcaoEstranhaQuantia(Action):

    def name(self) -> Text:
        return "action_opcao_estranha_quantia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            text = ['Quantas Peças']
            for texto in text:
                dispatcher.utter_message(texto)
            return []

class ActionRespostaForm(Action):

    def name(self) -> Text:
        return "resposta_escolha_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            tipo_produto = tracker.get_slot("produto")
            tipo_tamanho = tracker.get_slot("quantidade")
            qtd = tracker.get_slot("quantidade")
            qtdFinal = str(qtd)
            texto = f'Foi escolhido {qtdFinal} peças de {tipo_produto} tamanho {tipo_tamanho}. Mais algum produto?'
            dispatcher.utter_message(texto)
            return []       

class ActionLimpaSlots(Action):
    ##### Nome de actions para o rasa
    def name(self) -> Text:
        return "action_limpa_slots"
    ######## Zera os slots
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            return[SlotSet("produto",None),
                   SlotSet("tamanho",None),
                   SlotSet("quantidade",None)
                   ]