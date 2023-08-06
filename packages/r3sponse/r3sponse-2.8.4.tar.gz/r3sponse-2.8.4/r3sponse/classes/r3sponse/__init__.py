#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from r3sponse.classes.config import *
from r3sponse.classes import utils
from r3sponse.classes.utils import color, symbol
from r3sponse.classes import exceptions
from django.http import JsonResponse
import json as pypi_json
import traceback as _traceback_

# the manager class.
class R3sponse(object):
	def __init__(self):	

		# set log file.
		self.log_file = None

		# set log level.
		self.log_level = 0
		#if utils.argument_present('--log-level'):
		#	try: self.log_level = int(utils.get_argument('--log-level'))
		#	except: self.log_level = 0
		#
		self.ResponseObject = ResponseObject

	# response functions.
	def default_response(self, attributes={
		"success":False,
		"message":None,
		"error":None,
	}):
		return self.ResponseObject(attributes=attributes)
	def success(self,
		# the message (must be param #1).
		message, 
		# additional returnable functions (must be param #2).
		variables={}, 
		# log log level of the message (int).
		log_level=None, 
		# the required log level for when printed to console (leave None to use self.log_level).
		required_log_level=None, 
		# save the error to the logs file.
		save=False,
		# return as a django JsonResponse.
		django=False,
	):
		response = self.default_response({
			"success":True,
			"message":message,
			"error":None,
		})
		for key, value in variables.items():
			response[key] = value
		self.log(message=response["message"], log_level=log_level, save=save, required_log_level=required_log_level)
		if django: 
			try:
				response = JsonResponse(response.dict(), safe=False)
			except AttributeError:
				response = JsonResponse(response)
		return response
	def error(self,
		# the error message.
		error="", 
		# log log level of the message (int).
		log_level=None, 
		# the required log level for when printed to console (leave None to use self.log_level).
		required_log_level=None, 
		# save the error to the erros file.
		save=False,
		# return as a django JsonResponse.
		django=False,
		# raise error for developer traceback.
		traceback=ERROR_TRACEBACK,
	):
		response = self.default_response({
			"success":False,
			"message":None,
			"error":error,
		})
		self.log(error=response["error"], log_level=log_level, save=save, required_log_level=required_log_level)
		if traceback:
			raise ValueError(response["error"])
		if django: 
			try:
				response = JsonResponse(response.dict(), safe=False)
			except AttributeError:
				response = JsonResponse(response)
		return response
		#

	# parameter functions.
	def get_request_parameter(self, request, identifier, traceback=None):
		response = self.default_response()
		format = None
		if ":" in identifier:
			identifier,format = identifier.split(":")
			while True:
				if " " in format: format = format.replace(" ","")
				else: break
		if request.method in ["post", "POST"]:
			variable = request.POST.get(identifier)
		else:
			variable = request.GET.get(identifier)
		if variable in ["", None]:
			if traceback != None:
				return variable, self.error(f"{traceback}: Define parameter: [{identifier}].")
			else:
				return variable, self.error(f"Define parameter: [{identifier}].")

		elif format != None:
			if format in ["str", "string"]: variable = str(variable)
			elif format in ["int", "integer"]: variable = int(variable)
			elif format in ["bool", "boolean"]: 
				if variable in ["true", "True", "TRUE", True]: variable = True
				else: variable = False
			elif format in ["float", "double"]: variable = float(variable)
			elif format in ["array", "list"]: variable = variable.split(",")
			else:
				raise ValueError(f"Unrecognized <r3sponse.get_request_parameter> format: {format}.")
		return variable, self.success(f"Succesfully retrieved request parameter [{identifier}].", {
			"key":identifier,
			"value":variable,
		})
	def get_request_parameters(self, request, identifiers=[], optional=False, empty_value=None, traceback=None):
		if isinstance(identifiers, str):
			return self.error("__get_request_params__ is used to retrieve several identifiers (array format not string).")
		params = self.ResponseObject()
		for param in identifiers:
			param_value, response = self.get_request_parameter(request, param, traceback=traceback)
			param = param.split(":")[0]
			if response["error"] != None: 
				if optional:
					params[param] = empty_value
				else:
					return params, response
			else: 
				params[param] = param_value
		if optional:
			for key in identifiers:
				try: params[key]
				except: params[key] = empty_value
		return params, self.success(f"Succesfully retrieved {len(params)} request parameter(s).")

	# check parameters.
	def check_parameter(self, parameter=None, name="parameter", empty_value=None, traceback=None):
		response = self.default_response()
		if parameter == empty_value: 
			if traceback != None:
				return self.error(f"{traceback}: Define parameter [{name}].")
			else:
				return self.error(f"Define parameter [{name}].")
		if ":" in name:
			name,formats = name.split(":")
			while True:
				if " " in formats: formats = formats.replace(" ","")
				else: break
			formats = formats.split(",")
			param_format = Formats.get(parameter, serialize=True)
			if param_format not in formats:
				return self.error(f"Incorrect parameter [{name}:{param_format}] format, correct format(s): {Array(path=False, array=formats).string(joiner=', ')}.")
		return self.success(f"Succesfully checked parameter [{name}].")
	def check_parameters(self, parameters={"parameter":None}, empty_value=None, traceback=None):
		response = self.default_response()
		for id, value in parameters.items():
			response = self.check_parameter(value, id, empty_value=empty_value, traceback=traceback)
			if response["error"] != None: return response
		return response

	# log functions.
	def log(self, 
		# option 1:
		# the message (#1 param).
		message=None,
		# option 2:
		# the error.
		error=None,
		# option 3:
		# the response dict (leave message None to use).
		response={},
		# print the response as json.
		json=False,
		# optionals:
		# the log level for printing to console.
		log_level=0,
		# the required log level for when printed to console (leave None to use self.log_level).
		required_log_level=None, 
		# save to log file.
		save=False,
		# save errors only (for option 2 only).
		save_errors=False,
	):
		msg, _error_ = None, False
		if [message,error,response] == [None,None,{}]:
			raise ValueError("Define either parameter [message:str], [error:str] or [response:dict].")
		if response != {}:
			if response["error"] != None: 
				_error_ = True
				msg = f"Error: {response['error']}"
			else: 
				if response.__class__.__name__ in ["Output"]: 
					msg = str(response)
				else:
					msg = response["message"]
		elif error != None: 
			msg = f"Error: {error}"
		else: 
			msg = message
		if required_log_level == None: required_log_level = self.log_level
		try:
			required_log_level = int(required_log_level)
		except: 
			required_log_level = 0
		try:
			comparison = log_level != None and log_level >= required_log_level
		except TypeError as e:
			if "not supported between instances of 'dict' and 'int'" in f"{e}":
				raise TypeError(f"You most likely returned a r3sponse.error_response when you meant a r3sponse.success_response, error: {e}")
			else:
				raise TypeError(e)
		if comparison:
			#print(f"{Date().seconds_timestamp} - {color.fill(msg)}")
			if json:
				if response != {}:
					print(response.json())
				elif error != None:
					print(self.error(error))
				else:
					print(self.success(message))
			else:
				print(f"{color.fill(msg)}")
		if save: 
			self.__log_to_file__(msg)
		elif save_errors and _error_:
			self.__log_to_file__(msg)

		#
	def load_logs(self, format="webserver", options=["webserver", "cli", "array", "string"]):
		try:
			logs = Formats.File(self.log_file, load=True, blank="").data
		except:
			return self.error("Failed to load the logs.")
		if format == "webserver":
			logs = logs.replace("\n", "<br>")
		elif format == "cli":
			a=1
		elif format == "array" or format == list:
			logs = logs.split("\n")
		elif format == "string" or format == str:
			logs = str(logs)
		else: 
			return self.error(f"Invalid format parameter [{format}], valid options: {options}.")

		return self.success("Succesfully loaded the logs.", {"logs":logs})
	def reset_logs(self):
		Formats.File(self.log_file).save(f"Resetted log file.\n")
		#
	
	# system functions.
	def __log_to_file__(self, message):

		# init.
		response = self.default_response()
		try:
			with open(self.log_file, "a") as file:
				file.write(f'{Date().seconds_timestamp} - {message}\n')
			response["success"] = True
			response["message"] = "Succesfully logged the message."
		except:
			response["error"] = "Failed to log the message."
			return response
		
		# check file size.
		size = FilePath(self.log_file).size(mode="mb", format="integer")
		if size >= 100: self.reset_logs()

		# return response.
		return response

		#

	# a response object.
	def serialize(self, response={}):
		if isinstance(response, str):
			try:
				response = ast.literal_eval(response)
			except:
				response = json.loads(response)
		for key in list(response.keys()):
			value = response[key]
			no_dict = False
			if isinstance(value, dict):
				value = self.serialize(value)
			else:
				try:
					value = ast.literal_eval(value)
				except:
					try:
						value = json.loads(value)
					except:
						no_dict = True
				if no_dict == False and isinstance(value, dict):
					value = self.serialize(value)
			if no_dict == False: a=1
			elif value in [True, "True", "true", "TRUE"]: value = True
			elif value in [False, "False", "false", "FALSE"]: value = False
			elif isinstance(value, str):
				if "." in value:
					try: value = float(value)
					except: a=1
				else:
					try: value = int(value)
					except: a=1
			response[key] = value
		return response
	def response(self, response={
			"success":False,
			"message":None,
			"error":None,
	}):
		return self.ResponseObject(response)
	def safe_response(self, response={
			"success":False,
			"message":None,
			"error":None,
	}):
		return self.response(self.serialize(response))

# a response object.
class ResponseObject(object):
	def __init__(self, 
		# the response attributes.
		attributes={
			"success":False,
			"message":None,
			"error":None,
		},
		# import a dumped json response (str) (ignores attributes).
		json=None,
	):

		# check self instance.
		if isinstance(attributes, ResponseObject):
			#attributes = attributes.dict()
			#self = attributes
			attributes = attributes.dict()
		elif isinstance(json, ResponseObject):
			json = json.dict()

		# assign attributes.
		if json != None:
			if isinstance(json, str):
				try:
					self.assign(pypi_json.loads(json))
				except:
					try:
						self.assign(ast.literal_eval(json))
					except:
						self.assign(pypi_json.loads(String(json).slice_dict()))
			elif isinstance(json, dict):
				self.assign(json)
			elif json != None:
				raise exceptions.InvalidUsage("The r3sponse.ResponseObject json parameter must be str / dict format.")
		else:
			self.assign(attributes)

		# clean message & error.
		try:
			if self.message in ["None", "null", "", "nan"]: self.message = None
			if self.message != None:
				self.message = String(self.message).capitalized_word()
			if self.error in ["None", "null", "", "nan"]: self.error = None
			if self.error != None:
				self.error = String(self.error).capitalized_word()
			while True:
				if self.message != None and len(self.message) >= 1 and self.message[len(self.message)-1] in [" ", ".", ","]:
					self.message = self.message[:-1]
				elif self.error != None and len(self.error) >= 1 and self.error[len(self.error)-1] in [" ", ".", ","]:
					self.error = self.error[:-1]
				elif self.error != None and len(self.error) >= len("Error: ") and self.error[:len("Error: ")] in ["Error: "]:
					self.error = String(self.error[len("Error: "):]).capitalized_word()
				else: break
			
			# add dot.
			if self.message != None  and len(self.message) > 0 and self.message[len(self.message)-1] not in ["!", "?"]:
				self.message += "."
			if self.error != None  and len(self.error) > 0 and self.error[len(self.error)-1] not in ["!", "?"]:
				self.error += "."

			# check error passed as success response. & reversed
			if self.message != None and len(self.message) >= len("Failed") and self.message[:len("Failed")] == "Failed":
				#_traceback_.print_exc() 
				raise ValueError("A success response may not start with (failed ...). You most likely called an r3sponse.success return while you meant r3sponse.error.")
			if self.error != None and len(self.error) >= len("Success") and self.error[:len("Success")] == "Success":
				#_traceback_.print_exc() 
				raise ValueError("An error response may not start with (success ...). You most likely called an r3sponse.error return while you meant r3sponse.success.")
		
		# except if not present.
		except AttributeError: a=1
	# clean default values.
	def clean(self):
		for i in ["error", "message", "success"]:
			del self[i]
			#except: a=1
		return self
	# assign dict.
	def assign(self, dictionary):
		if isinstance(dictionary, (dict, Dictionary)):
			for key,value in dictionary.items():
				self[key] = value
		elif isinstance(dictionary, (tuple, list, Array)):
			for key,value in dictionary:
				self[key] = value
		else:
			raise exceptions.InvalidUsage("The dictionary parameter must be a dict or tuple.")
		return self
	# crash the error message.
	def crash(self, error="ValueError", traceback=True, json=False):
		if json:
			self.log(error=self["error"], json=json)
			sys.exit(1)
		else:
			#if not traceback:
			#	sys.tracebacklimit = 0
			#else:
			#	sys.tracebacklimit = 1
			if error.lower() in ["valueerror", "value_error"]: raise ValueError(self["error"])
			else: raise Exception(self["error"])
	def unpack(self, 
		# the key / keys / defaults parameter (#1).
		# str instance:
		#   unpack the str key
		# list instance:
		#   unpack all keys in the list.
		# dict instance:
		#   unpack all keys from the dict & when not present return the key's value as default.
		keys,
	):
		defaults = {}
		if isinstance(keys, (dict, Files.Dictionary, ResponseObject)):
			if isinstance(keys, dict):
				defaults = dict(keys)
				keys = list(keys.keys())
			else:
				defaults = keys.dict()
				keys = keys.keys()
		elif isinstance(keys, str):
			keys = [keys]
		unpacked = []
		for key in keys:
			value, set = None, True
			try: 
				value = self[key]
			except KeyError: 
				try:
					value = defaults[key]
				except KeyError: 
					set = False
			if not set:
				raise exceptions.UnpackError(f"Dictionary does not contain attribute [{key}].")
			unpacked.append(value)
		return unpacked
	def remove(self, keys=[], values=[], save=False):
		for i in keys:
			try: del self[i]
			except: a=1
		if values != []:
			new = {}
			for k,v in self.iterate():
				if v not in values: new[k] = v
			self.assign(new)
		if save: self.save()
		return self
	# iterations.
	def iterate(self, sorted=False, reversed=False):
		return self.items(reversed=reversed, sorted=sorted)
	def items(self, sorted=False, reversed=False, dictionary=None):
		if dictionary == None:
			dictionary = self.dict()
		if sorted: dictionary = self.sort()
		if reversed: return self.reversed().items()
		else: return dictionary.items()
	def keys(self, sorted=False, reversed=False):
		if sorted:
			return self.sort(self.keys(sorted=False, reversed=reversed))
		if reversed: 
			keys = list(vars(self))
			reversed_keys = []
			c = len(keys)-1
			for _ in range(len(keys)):
				reversed_keys.append(keys[c])
				c -= 1
			return reversed_keys
		else: return list(vars(self))
	def values(self, sorted=False, reversed=False, dictionary=None):
		if dictionary == None: dictionary = self.dict()
		if sorted:
			return self.sort(self.values(sorted=False, reversed=reversed, dictionary=dictionary))
		values = []
		for key, value in self.items(reversed=reversed, dictionary=dictionary):
			values.append(value)
		return values
	def reversed(self, dictionary=None):
		if dictionary == None: dictionary = self.dict()
		reversed_dict = []
		for key in self.keys(reversed=True, dictionary=dictionary):
			reversed_dict[key] = dictionary[key]
		return reversed_dict
	def sort(self, alphabetical=True, ascending=False, reversed=False, dictionary=None):
		if dictionary == None: dictionary = self.dict()
		new = {}
		if alphabetical or ascending:
			_sorted_ = Array(path=False, array=list(dictionary.keys())).sort(alphabetical=alphabetical, ascending=ascending, reversed=reversed)
		else: raise ValueError("Unknown behaviour, alphabetical=False.")
		for key in _sorted_:
			new[Formats.denitialize(key)] = dictionary[Formats.denitialize(key)]
		return new
	# return self as dict.
	def dict(self, sorted=False, reversed=False, json=False):
		dictionary = {}
		for key in self.keys():
			dictionary[Formats.denitialize(key)] = self[Formats.denitialize(key)]
		return self.serialize(json=json, sorted=sorted, reversed=reversed, dictionary=dictionary)
	# dump json string.
	def json(self, sorted=False, reversed=False, indent=4, dictionary=None, ):
		if dictionary == None: dictionary = self.dict()
		return json.dumps(self.serialize(json=False, sorted=sorted, reversed=reversed, dictionary=dictionary), indent=indent).replace(': "False"', ': false').replace(': "True"', ': true').replace(': "None"', ': null')
	# serialize dict.
	def serialize(self, sorted=False, reversed=False, json=False, dictionary=None):
		if dictionary == None: dictionary = self.dict()
		if isinstance(dictionary, Dictionary):
			dictionary = dictionary.dictionary
		if sorted:
			items = self.items(reversed=reversed, dictionary=self.sort(alphabetical=True, dictionary=dictionary))
		else:
			items = self.items(reversed=reversed, dictionary=dictionary)
		dictionary = {}
		for key, value in items:
			value = Formats.denitialize(value)
			if isinstance(value, (dict, Dictionary)):
				value = self.serialize(json=json, sorted=sorted, reversed=reversed, dictionary=value)
			elif isinstance(value, (list, Array)):
				value = Array(value).serialize(json=json, sorted=sorted, reversed=reversed)
			elif isinstance(value, object):
				value = str(value)
			elif isinstance(value, str) or isinstance(value, bool) or value == None:
				if value in [True, "True", "True".lower()]: 
					if json:
						value = "true"
					else: 
						value = True
				elif value in [False, "False", "False".lower()]: 
					if json:
						value = "false"
					else: 
						value = False
				elif value in [None, "None", "None".lower()]: 
					if json:
						value = "null"
					else: 
						value = None
			dictionary[key] = value
		return dictionary
	# support default iteration.
	def __iter__(self):
		return iter(self.keys())
	# support '>=' & '>' operator.
	def __gt__(self, response):
		if not isinstance(directory, self.__class__):
			raise exceptions.FormatError(f"Can not compare object {self.__class__} & {response.__class__}.")
		return len(self) > len(response)
	def __ge__(self, response):
		if not isinstance(response, self.__class__):
			raise exceptions.FormatError(f"Can not compare object {self.__class__} & {response.__class__}.")
		return len(self) >= len(response)
	# support '<=' & '<' operator.
	def __lt__(self, response):
		if not isinstance(response, self.__class__):
			raise exceptions.FormatError(f"Can not compare object {self.__class__} & {response.__class__}.")
		return len(self) < len(response)
	def __le__(self, response):
		if not isinstance(response, self.__class__):
			raise exceptions.FormatError(f"Can not compare object {self.__class__} & {response.__class__}.")
		return len(self) <= len(response)
	# support '==' & '!=' operator.
	def __eq__(self, dictionary):
		if isinstance(dictionary, dict):
			return str(self.sort()) == str(Dictionary(dictionary).sort())
		elif isinstance(dictionary, Dictionary):
			return str(self.sort()) == str(dictionary.sort())
		else:
			try:
				return str(self.sort()) == str(dictionary.sort())
			except:
				return False
	def __ne__(self, dictionary):
		if isinstance(dictionary, dict):
			return str(self.sort()) != str(Dictionary(dictionary).sort())
		elif isinstance(dictionary, Dictionary):
			return str(self.sort()) != str(dictionary.sort())
		else:
			try:
				return str(self.sort()) != str(dictionary.sort())
			except:
				return False
	# support 'in' operator.
	def __contains__(self, response):
		keys = self.keys()
		if isinstance(response, (list, Array)):
			for i in response:
				if response in keys:
					return True
			return False
		else:
			return response in keys
	# support item assignment.
	def __setitem__(self, key, value):
		setattr(self, key, value)
	def __getitem__(self, key):
		return getattr(self, key)
	def __delitem__(self, key):
		delattr(self, key)
	# str representable.
	def __str__(self):
		return self.json(indent=4) 
	# bool representable.
	def __bool__(self):
		return self.success
		#
	# content count.
	def __len__(self):
		return len(self.keys())
	# object id.
	def __id__(self):
		return f"({self.instance()}:{str(self)})"
	# object instance.
	def instance(self):
		return "ResponseObject"
	@property
	def __name__(self):
		return self.instance()
	# return raw data.
	def raw(self):
		return self.dict()

# initialized objects.
r3sponse = R3sponse()
