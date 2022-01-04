import re
import retry
import npu


class ChatAI(object):
    def __init__(self, model):
        self.bot_name = "Chris"
        self.chat_history = [
            "User: hi",
            "{bot_name}: Hello there! I'm Chris. I work as a coder but I love rock climbing. What about you?",
            "User: hi chris, nice to meet you",
            "{bot_name}: Nice to meet you! How are you feeling today?",
        ]
        self.max_history = 104
        self.model = model
        self.prompt = "Chris is a 30 year old male software developer.  He is also a Christian and likes to give people good advice.  Chris speaks softly and politely. Chris is friendly.  Chris wants to be User's friend."

    def get_resp(self, input_message):
        """"
        When we send a request the chat_history has to look like below for
        the model to know it is the bot speaking:
        User: input_message
        {bot_name}:
        """
        self._update_chat_history(message=input_message, sender="User")
        self._update_chat_history(message="", sender="{bot_name}")

        request = self._prepare_request()
        raw_response = self.model.request(request)
        formatted_response = self._format_model_response(raw_response)

        self.chat_history[-1] += formatted_response
        return formatted_response
        
    def _prepare_request(self):
        formatted_chat_history = self.chat_history[-self.max_history :]
        formatted_chat_history = "\n".join(formatted_chat_history)
        request = self.prompt + formatted_chat_history
        request = request.replace("{bot_name}", self.bot_name)
        return request

    def _format_model_response(self, resp):
        partial_chat = re.split(
            "User|{lower_bot_name}:|{bot_name}:|\n|\$".format(
                lower_bot_name=self.bot_name.lower(), bot_name=self.bot_name
            ),
            resp,
        )[0]
        partial_chat = partial_chat.strip(" ")
        if len(partial_chat) == 0:
            partial_chat = "..."
        return partial_chat

    def _update_chat_history(self, message, sender):
        cleaned_message = message.strip(" ")
        self.chat_history += [f"{sender}: {cleaned_message}"]
        
        
class FineTunedAPI(object):
    def __init__(self, temp, rep_penalty):
        API_TOKEN = "<EMAIL dev@chai.ml to request token>"
        npu.api(API_TOKEN, deployed=True)
        self.temp = temp
        self.rep_penalty = rep_penalty

    @retry.retry(tries=3, backoff=2)
    def request(self, data):
        data = data[-2048:]
        kwargs = {
            "remove_input": True,  # whether to return your input
            "do_sample": True,  # important to get realistic sentences and not just MLE
            "temperature": self.temp,
            "response_length": 32,  # how many response tokens to generate
            "repetition_penalty": self.rep_penalty,  # 1 is the default
            "eos_token_id": 198,  # this is \n
        }
        model_id = "<EMAIL dev@chai.ml to request model ID>"
        output = npu.predict(model_id, [data], kwargs)
        resp = output[0]["generated_text"]
        return resp
