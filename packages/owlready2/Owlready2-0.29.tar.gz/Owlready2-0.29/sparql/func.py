# Owlready2
# Copyright (C) 2021 Jean-Baptiste LAMY
# LIMICS (Laboratoire d'informatique médicale et d'ingénierie des connaissances en santé), UMR_S 1142
# University Paris 13, Sorbonne paris-Cité, Bobigny, France

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys, os, re, urllib.parse, functools, datetime
from owlready2.base import _universal_datatype_2_abbrev, _parse_datetime
import owlready2, owlready2.rply as rply


_BOOL_EXPRESSION_MEMBERS   = { "||", "&&", "=", "COMPARATOR", "LIST_COMPARATOR", "BOOL" }
_NUMBER_EXPRESSION_MEMBERS = { "*", "/", "+", "-" }
_FUNC_2_DATATYPE = {
  "STR" : _universal_datatype_2_abbrev[str], # ok
  "LANG" : _universal_datatype_2_abbrev[str], # ok
  "LANGMATCHES" : _universal_datatype_2_abbrev[bool], # ok
  "DATATYPE" : None, # => objs # ok
  "BOUND" : _universal_datatype_2_abbrev[bool], # ok
  "IRI" : None, # ok
  "URI" : None, # ok
  "BNODE" : None, # ok
  "RAND" : _universal_datatype_2_abbrev[float], # ok
  "ABS" : 0, # => Auto (= int or float or str without lang) # ok
  "CEIL" : _universal_datatype_2_abbrev[float], # ok
  "FLOOR" : _universal_datatype_2_abbrev[float], # ok
  "ROUND" : _universal_datatype_2_abbrev[int], # ok
  #"CONCAT" :  # ok
  "STRLEN" : _universal_datatype_2_abbrev[int], # ok
  #"UCASE" :  # ok
  #"LCASE" :  # ok
  "ENCODE_FOR_URI" : _universal_datatype_2_abbrev[str], # ok
  "CONTAINS" : _universal_datatype_2_abbrev[bool], # ok
  "STRSTARTS" : _universal_datatype_2_abbrev[bool], # ok
  "STRENDS" : _universal_datatype_2_abbrev[bool], # ok
  #"STRBEFORE" :  # ok
  #"STRAFTER" :  # ok
  "YEAR" : _universal_datatype_2_abbrev[int], # ok
  "MONTH" : _universal_datatype_2_abbrev[int], # ok
  "DAY" : _universal_datatype_2_abbrev[int], # ok
  "HOURS" : _universal_datatype_2_abbrev[int], # ok
  "MINUTES" : _universal_datatype_2_abbrev[int], # ok
  "SECONDS" : _universal_datatype_2_abbrev[float], # ok
  "TIMEZONE" : _universal_datatype_2_abbrev[str], # ok
  "TZ" : _universal_datatype_2_abbrev[str], # ok
  "NOW" : _universal_datatype_2_abbrev[datetime.datetime], # ok
  "UUID" : None, # ok
  "STRUUID" : _universal_datatype_2_abbrev[str], # ok
  "MD5" : _universal_datatype_2_abbrev[str], # ok
  "SHA1" : _universal_datatype_2_abbrev[str], # ok
  "SHA256" : _universal_datatype_2_abbrev[str], # ok
  "SHA384" : _universal_datatype_2_abbrev[str], # ok
  "SHA512" : _universal_datatype_2_abbrev[str], # ok
  "COALESCE" : 0, # ok
  #"IF" :  # ok
  #"STRLANG" :  # ok
  #"STRDT" :  # ok
  "SAMETERM" : _universal_datatype_2_abbrev[bool], # ok
  "ISIRI" : _universal_datatype_2_abbrev[bool], # ok
  "ISURI" : _universal_datatype_2_abbrev[bool], # ok
  "ISBLANK" : _universal_datatype_2_abbrev[bool], # ok
  "ISLITERAL" : _universal_datatype_2_abbrev[bool], # ok
  "ISNUMERIC" : _universal_datatype_2_abbrev[bool], # ok
  "REGEX" : _universal_datatype_2_abbrev[bool],
  #"SUBSTR" :  # ok
  #"REPLACE" :  # ok
  #"SIMPLEREPLACE" :  # ok
  "NEWINSTANCEIRI" : None, # ok
  }


import hashlib, uuid
def _md5    (x): return hashlib.md5   (x.encode("utf8")).hexdigest()
def _sha1   (x): return hashlib.sha1  (x.encode("utf8")).hexdigest()
def _sha256 (x): return hashlib.sha256(x.encode("utf8")).hexdigest()
def _sha384 (x): return hashlib.sha384(x.encode("utf8")).hexdigest()
def _sha512 (x): return hashlib.sha512(x.encode("utf8")).hexdigest()
def _struuid(x): return str(uuid.uuid4())
def _uuid   (x): return _CURRENT_TRANSLATOR.get().world._abbreviate(str(uuid.uuid4()))

def _seconds(x):
  try: d = _parse_datetime(x)
  except ValueError: return 0.0
  return d.second + d.microsecond / 1000000.0

def _tz(x):
  try: d = _parse_datetime(x)
  except ValueError: return ""
  z = d.tzinfo.tzname(d)
  if z.startswith("UTC"): z = z[3:]
  return z


@functools.lru_cache(maxsize=128)
def _get_regexp(pattern, flags):
  f = 0
  for i in flags:
    if   i == "i": f |= re.IGNORECASE
    elif i == "s": f |= re.DOTALL
    elif i == "m": f |= re.MULTILINE
  return re.compile(pattern, f)

def _regex(s, pattern, flags):
  pattern = _get_regexp(pattern, flags)
  return bool(pattern.search(s))

_REGEX_SUB_ARG_RE = re.compile("\\$([0-9]*)")
def _sparql_replace(s, pattern, replacement, flags):
  pattern = _get_regexp(pattern, flags)
  replacement = _REGEX_SUB_ARG_RE.sub(r"\\\1", replacement)
  return pattern.sub(replacement, s)
  
def _timezone(x):
  delta = _parse_datetime(x).utcoffset()
  if delta.days < 0:
    seconds = -24 * 60 * 60 * delta.days - delta.seconds
    days    = 0
    sign    = "-"
  else:
    seconds = delta.seconds
    days    = delta.days
    sign    = ""
    
  hours = seconds / (60 * 60)
  minutes = (seconds - hours * 60 * 60) / 60
  seconds = seconds - hours * 60 * 60 - minutes * 60
  
  return "%sP%sT%s%s%s" % (
    sign,
    "%dD" % days if days else "",
    "%dH" % hours if hours else  "",
    "%dM" % minutes if minutes else  "",
    "%dS" % delta.seconds if (not days and not hours and not minutes) else "",
  )
  
class _Func(object):
  def __init__(self, world):
    self.world        = world
    self.last_nb_call = -1
    self.bns          = {}
    self.now          = None

  def _check_reset(self):
    if self.world._nb_sparql_call != self.last_nb_call:
      self.last_nb_call = self.world._nb_sparql_call
      self.bns = {}
      self.now = None
      
  def _now(self):
    self._check_reset()
    if self.now is None: self.now = datetime.datetime.now().isoformat()
    return self.now
  
  def _bnode(self, x):
    self._check_reset()
    bn = self.bns.get(x)
    if not bn: bn = self.bns[x] = self.world.new_blank_node()
    return bn
  
  def _newinstanceiri(self, x):
    x = self.world._get_by_storid(x)
    namespace = (owlready2.CURRENT_NAMESPACES.get() and owlready2.CURRENT_NAMESPACES.get()[-1]) or x.namespace
    iri = self.world.graph._new_numbered_iri("%s%s" % (namespace.base_iri, x.name.lower()))
    return self.world._abbreviate(iri)
  
  
def register_python_function(world):
  world.graph.db.create_function("md5",            1, _md5,      deterministic = True)
  world.graph.db.create_function("sha1",           1, _sha1,     deterministic = True)
  world.graph.db.create_function("sha256",         1, _sha256,   deterministic = True)
  world.graph.db.create_function("sha384",         1, _sha384,   deterministic = True)
  world.graph.db.create_function("sha512",         1, _sha512,   deterministic = True)
  world.graph.db.create_function("seconds",        1, _seconds,  deterministic = True)
  world.graph.db.create_function("tz",             1, _tz,       deterministic = True)
  world.graph.db.create_function("timezone",       1, _timezone, deterministic = True)
  world.graph.db.create_function("encode_for_uri", 1, urllib.parse.quote, deterministic = True)
  world.graph.db.create_function("uuid",           1, _uuid)
  world.graph.db.create_function("struuid",        1, _struuid)
  world.graph.db.create_function("regex",         -1, _regex,          deterministic = True)
  world.graph.db.create_function("sparql_replace",-1, _sparql_replace, deterministic = True)
  
  world._nb_sparql_call = 0
  func = _Func(world)
  world.graph.db.create_function("now",             0, func._now, deterministic = True)
  world.graph.db.create_function("bnode",          -1, func._bnode)
  world.graph.db.create_function("newinstanceiri",  1, func._newinstanceiri)
  
  
class FuncSupport(object):
  def parse_expression(self, expression):
    if   hasattr(expression, "sql"):   return " %s" % expression.sql
    elif isinstance(expression, list):
      if expression:
        if isinstance(expression[0], rply.Token) and expression[0].name == "FUNC":
          func = expression[0].value.upper()
          if   func == "CONTAINS":
            return "(INSTR(%s)!=0)" % self.parse_expression(expression[2])
          elif func == "STRSTARTS":
            return "(INSTR(%s)=1)" % self.parse_expression(expression[2])
          elif func == "STRENDS":
            eo1 = self.parse_expression(expression[2][0])
            eo2 = self.parse_expression(expression[2][2])
            return "(SUBSTR(%s,-LENGTH(%s))=%s)" % (eo1, eo2, eo2)
          elif func == "STRBEFORE":
            eo1 = self.parse_expression(expression[2][0])
            eo2 = self.parse_expression(expression[2][2])
            return "SUBSTR(%s,1,INSTR(%s,%s)-1)" % (eo1, eo1, eo2)
          elif func == "STRAFTER":
            eo1 = self.parse_expression(expression[2][0])
            eo2 = self.parse_expression(expression[2][2])
            return "IIF(INSTR(%s,%s)=0,'',SUBSTR(%s,INSTR(%s,%s)+1))" % (eo1, eo2, eo1, eo1, eo2)
          elif func == "STR":
            type, datatype = self.infer_expression_type(expression[2])
            if   type == "objs":
              return "'<'||(SELECT iri FROM resources WHERE storid=%s)||'>'" % self.parse_expression(expression[2])
            elif type == "datas":
              return "''||%s" % self.parse_expression(expression[2])
            else: # quads
              eo = self.parse_expression(expression[2])
              if not eo.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of STR(%s)!" % eo)
              ed = eo[:-1] + "d"
              return "IIF(%s IS NULL, '<'||(SELECT iri FROM resources WHERE storid=%s)||'>', ''||%s)" % (ed, eo, eo)
          elif (func == "IRI") or (func == "URI"):
            type, datatype = self.infer_expression_type(expression[2])
            if   type == "objs":
              return self.parse_expression(expression[2])
            elif type == "datas":
              return "(SELECT storid FROM resources WHERE iri=RTRIM(TRIM(%s,'<'),'>'))" % self.parse_expression(expression[2])
            else:
              eo = self.parse_expression(expression[2])
              if not eo.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of IRI(%s)!" % eo)
              ed = eo[:-1] + "d"
              return "IIF(%s IS NULL, %s, (SELECT storid FROM resources WHERE iri=RTRIM(TRIM(%s,'<'),'>')))" % (ed, eo, eo)
          elif func == "LANG":
            eo = self.parse_expression(expression[2])
            if not eo.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of LANG(%s)!" % eo)
            ed = eo[:-1] + "d"
            return "IIF(SUBSTR(%s, 1, 1)='@', SUBSTR(%s, 2), '')" % (ed, ed)
          elif (func == "ISIRI") or (func == "ISURI"):
            eo = self.parse_expression(expression[2])
            if not eo.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of ISIRI(%s)!" % eo)
            ed = eo[:-1] + "d"
            return "(%s IS NULL) & (%s > 0)" % (ed, eo)
          elif func == "ISBLANK":
            eo = self.parse_expression(expression[2])
            if not eo.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of ISBLANK(%s)!" % eo)
            ed = eo[:-1] + "d"
            return "(%s IS NULL) & (%s < 0)" % (ed, eo)
          elif func == "ISLITERAL":
            eo = self.parse_expression(expression[2])
            if not eo.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of ISLITERAL(%s)!" % eo)
            ed = eo[:-1] + "d"
            return "NOT(%s IS NULL)" % ed
          elif func == "ISNUMERIC":
            eo = self.parse_expression(expression[2])
            if not eo.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of ISNUMERIC(%s)!" % eo)
            ed = eo[:-1] + "d"
            return "(%s IN (43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 58, 59))" % ed
          elif func == "SAMETERM":
            eo1 = self.parse_expression(expression[2][0])
            eo2 = self.parse_expression(expression[2][2])
            return "(%s = %s)" % (eo1, eo2)
          elif func == "DATATYPE":
            eo = self.parse_expression(expression[2])
            if not eo.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of DATATYPE(%s)!" % eo)
            ed = eo[:-1] + "d"
            return "IIF(TYPEOF(%s)='integer', %s, %s)" % (ed, ed, owlready2.rdf_langstring)
          elif func == "BOUND":
            return "(%s IS NOT NULL)" % self.parse_expression(expression[2])
          elif func == "YEAR":
            return "CAST(SUBSTR(%s, 1, 4) AS INTEGER)" % self.parse_expression(expression[2])
          elif func == "MONTH":
            return "CAST(SUBSTR(%s, 6, 2) AS INTEGER)" % self.parse_expression(expression[2])
          elif func == "DAY":
            return "CAST(SUBSTR(%s, 9, 2) AS INTEGER)" % self.parse_expression(expression[2])
          elif func == "HOURS":
            return "CAST(SUBSTR(%s, 12, 2) AS INTEGER)" % self.parse_expression(expression[2])
          elif func == "MINUTES":
            return "CAST(SUBSTR(%s, 15, 2) AS INTEGER)" % self.parse_expression(expression[2])
          #elif func == "SECONDS":
          #  return "CAST(SUBSTR(%s, 18, 2) AS INTEGER)" % self.parse_expression(expression[2])
          elif func == "CEIL":
            eo = self.parse_expression(expression[2])
            return "(CAST(%s AS INTEGER)+IIF(%s<0.0,0.0,IIF(CAST(%s AS INTEGER)=%s,0.0,1.0)))" % (eo, eo, eo, eo)
          elif func == "FLOOR":
            eo = self.parse_expression(expression[2])
            return "(CAST(%s AS INTEGER)+IIF(%s<0.0,IIF(CAST(%s AS INTEGER)=%s,0.0,-1.0),0.0))" % (eo, eo, eo, eo)
          elif func == "RAND":
            return "((RANDOM() + 9223372036854775808) / 18446744073709551615)"
          elif func == "LANGMATCHES":
            eo1 = self.parse_expression(expression[2][0])
            eo2 = self.parse_expression(expression[2][2]).strip()
            if not eo1.endswith("o"): raise ValueError("Cannot obtain the datatype of the parameter of LANGMATCHES(%s,%s)!" % (eo1, eo2))
            ed1 = eo1[:-1] + "d"
            if   eo2 == "'*'":
              return "TYPEOF(%s)='text'" % ed1
            elif eo2.startswith("'") and (len(eo2) <= 4):
              return "SUBSTR(%s,2,2)=LOWER(%s)" % (ed1, eo2)
            else:
              return "IIF(%s='*',TYPEOF(%s)='text',SUBSTR(%s,2,2)=LOWER(%s))" % (eo2, ed1, ed1, eo2)
          elif func == "STRDT":
            return self.parse_expression(expression[2][0])
          elif func == "STRLANG":
            return self.parse_expression(expression[2][0])
          
        return "".join(self.parse_expression(i) for i in expression) 
    elif expression is None: pass
    elif expression.name  == "VAR":    return self.parse_var(expression).bindings[0]
    elif expression.name  == "ARG":    self.parameters.append(expression.number); return "?" # XXX
    elif expression.value == "(":      return "("
    elif expression.value == ")":      return ")"
    else:                              return " %s" % expression.value
    return ""
  
  def infer_expression_type(self, expression):
    if isinstance(expression, list):
      if expression and isinstance(expression[0], rply.Token) and (expression[0].name == "FUNC"):
        func = expression[0].value.upper()
        if   func == "IF":
          a1, a2 = self.infer_expression_type(expression[2][2])
          b1, b2 = self.infer_expression_type(expression[2][4])
          if a1 != b1: return "quads", 0
          if a2 != b2: return a1, 0
          return a1, a2
        elif func == "CONCAT":
          d = 0
          for i, arg in enumerate(expression[2]):
            if i % 2 != 0: continue
            d = self.infer_expression_type(arg)[1]
            if isinstance(d, str): break
          return "datas", d
        elif (func == "UCASE") or (func == "LCASE") or (func == "STRBEFORE") or (func == "STRAFTER") or (func == "SUBSTR") or (func == "REPLACE") or (func == "SIMPLEREPLACE") or (func == ""):
          return self.infer_expression_type(expression[2][0])
        elif func == "STRDT":
          return "datas", self.parse_expression(expression[2][2])
        elif func == "STRLANG":
          return "datas", "'@'||%s" % self.parse_expression(expression[2][2])
        elif func == "TIMEZONE":
          return "datas", self.translator.world._abbreviate("http://www.w3.org/2001/XMLSchema#dayTimeDuration")
        else:
          func = expression[0].value.upper()
          if func in _FUNC_2_DATATYPE:
            datatype = _FUNC_2_DATATYPE[func]
            if datatype is None: return "objs", None
            return "datas", datatype
          return "quads", 0
        
      for i in expression:
        name = getattr(i, "name", "")
        if name in _BOOL_EXPRESSION_MEMBERS:   return "datas", _universal_datatype_2_abbrev[bool]
        if name in _NUMBER_EXPRESSION_MEMBERS: return "datas", 0
      r1 = set()
      r2 = set()
      for i in expression:
        if isinstance(i, list) and not i: continue
        a1, a2 = self.infer_expression_type(i)
        if not a1 is None:
          r1.add(a1)
          r2.add(a2)
      if len(r1) != 1: return "quads", 0
      if len(r2) != 1: return tuple(r1)[0], 0
      return tuple(r1)[0], tuple(r2)[0]
    
    elif  expression is None: pass
    elif  expression.name == "STRING":  return "datas", _universal_datatype_2_abbrev[str]
    elif  expression.name == "INTEGER": return "datas", _universal_datatype_2_abbrev[int]
    elif (expression.name == "FLOAT") or (expression.name == "DECIMAL"): return "datas", _universal_datatype_2_abbrev[float]
    elif  expression.name == "VAR":
      var = self.parse_var(expression)
      if var.type == "objs": return "objs", None
      return var.type, "%sd" % var.bindings[0][:-1]
    elif  expression.name == "ARG": # XXX
      return "quads", 0
    return None, None
    
