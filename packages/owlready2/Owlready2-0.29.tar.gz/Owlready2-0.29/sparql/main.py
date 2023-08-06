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


import sys, os
from owlready2 import *

"""

Not supported:

ASK
DESCRIBE
LOAD, ADD, MOVE, COPY, CLEAR, DROP

GRAPH, FROM, FROM NAMED

CONSTRUCT

SERVICE

INSERT DATA, DELETE DATA, DELETE WHERE (use INSERT or DELETE instead)

VALUES

nested SELECT queries

"""

from owlready2.sparql.parser import *
from owlready2.sparql.func   import *


class Translator(object):
  def __init__(self, world, error_on_undefined_entities = True):
    self.world                         = world
    self.error_on_undefined_entities   = error_on_undefined_entities
    self.prefixes                      = { "rdf:" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdfs:" : "http://www.w3.org/2000/01/rdf-schema#", "owl:" : "http://www.w3.org/2002/07/owl#", "xsd:" : "http://www.w3.org/2001/XMLSchema#", "owlready:" : "http://www.lesfleursdunormal.fr/static/_downloads/owlready_ontology.owl#" }
    self.base_iri                      = ""
    self.current_anonynous_var         = 0
    self.current_parameter             = -1
    self.has_parameter                 = False
    self.main_query                    = None
    self.preliminary_selects           = []
    self.recursive_preliminary_selects = {}
    self.parameters                    = []
    
    if not getattr(world.graph, "_has_sparql_func", False):
      register_python_function(world)
      world.graph._has_sparql_func = True
      
  def parse(self, sparql):
    CURRENT_TRANSLATOR.set(self)
    self.main_query = PARSER.parse(LEXER.lex(sparql))
    return PreparedQuery(self.world, self.sql(), [column.var for column in self.main_query.columns if not column.name.endswith("d")], [column.type for column in self.main_query.columns])
  
  def new_sql_query(self, name, block, selects = None, distinct = None, solution_modifier = None, preliminary = False, extra_binds = None):
    if preliminary and not name: name = "prelim%s" % (len(self.preliminary_selects) + 1)

    if isinstance(block, UnionBlock) and block.simple_union_triples:
      block = SimpleTripleBlock(block.simple_union_triples)
      
    if   isinstance(block, SimpleTripleBlock):
      s = SQLQuery(name)
      
    elif isinstance(block, UnionBlock):
      s = SQLCompoundQuery(name)
      if selects is None: selects = block.get_ordered_vars()
      
    elif isinstance(block, ExistsBlock):
      s = SQLQuery(name)
      
    else:
      raise ValueError("Unknown block type '%s'!" % block)
    
    if preliminary:
      s.preliminary = True
      self.preliminary_selects.append(s)
      
    extra_binds = extra_binds or []
    if isinstance(selects, list): # Otherwise, it is "SELECT *"
      for i, select in enumerate(selects):
        if isinstance(select, list): # ( expression AS var )
          selects[i] = select[2]
          bind = Bind(select[0], select[2])
          extra_binds.append(bind)
          
          
    if   isinstance(block, SimpleTripleBlock) or isinstance(block, ExistsBlock):
      s.parse_distinct(distinct)
      
      for i in block:
        if isinstance(i, Bind): s.prepare_bind(i)
      for bind in extra_binds: s.prepare_bind(bind)
      
      s.parse_selects(selects)
      
      s.parse_triples(block)
      for bind in extra_binds: s.parse_bind(bind)
      
      s.finalize_columns()
      
    elif isinstance(block, UnionBlock):
      for alternative in block:
        query = self.new_sql_query(None, alternative, selects, distinct, None, False, extra_binds)
        s.append(query, "UNION")
        
      s.columns = s.queries[0].columns
      
    if (not preliminary) and solution_modifier: self.solution_modifier = solution_modifier
    return s

  
  def expand_prefix(self, prefix):
    expanded = self.prefixes.get(prefix)
    if expanded: return expanded
    prefix0 = prefix[:-1] # Remove trailing :
    for ontology in self.world.ontologies.values():
      if prefix0 == ontology.name:
        self.prefixes[prefix] = ontology.base_iri
        return ontology.base_iri
    raise ValueError("Undefined prefix '%s'!" % prefix)

  def abbreviate(self, entity):
    if self.error_on_undefined_entities:
      r = self.world._abbreviate(entity, False)
      if r is None: raise ValueError("No existing entity for IRI '%s'! (use error_on_undefined_entities=False to accept unknown entities in SPARQL queries)" % entity)
      return r
    else:
      return self.world._abbreviate(entity)
    
  def sql(self):
    sql = ""
    if self.preliminary_selects:
      sql += "WITH "
      if max(prelim.recursive for prelim in self.preliminary_selects): sql += "RECURSIVE "
      sql += ",\n\n".join(prelim.sql() for prelim in self.preliminary_selects)
      sql += "\n\n"
    sql += self.main_query.sql()
    
    if self.solution_modifier[3]: sql += " LIMIT %s"  % self._to_sql(self.solution_modifier[3])
    if self.solution_modifier[4]:
      if not self.solution_modifier[3]: sql += " LIMIT -1" # SQLite requires a LIMIT clause before the OFFSET clause
      sql += " OFFSET %s" % self._to_sql(self.solution_modifier[4])
      
    return sql
  
  def _to_sql(self, x):
    if x.name == "ARG":
      self.parameters.append(x.number)
      return "?"
    return x.value
    
  def new_var(self):
    self.current_anonynous_var += 1
    return "??anon%s" % self.current_anonynous_var

  def new_parameter(self):
    self.current_parameter += 1
    return self.current_parameter
  
  def get_recursive_preliminary_select(self, triple, fixed, fixed_var, prelim_triples):
    prelim = self.recursive_preliminary_selects.get((triple, fixed, fixed_var, tuple(prelim_triples)))
    if not prelim:
      self.recursive_preliminary_selects[triple, fixed, fixed_var, tuple(prelim_triples)] = prelim = SQLRecursivePreliminaryQuery("prelim%s" % (len(self.preliminary_selects) + 1), triple, fixed, fixed_var)
      self.preliminary_selects.append(prelim)
      prelim.build(triple, prelim_triples)
    return prelim

  
  
class PreparedQuery(object):
  def __init__(self, world, sql, column_names, column_types):
    self.world        = world
    self.sql          = sql
    self.column_names = column_names
    self.column_types = column_types
    
  def execute(self, params = ()):
    self.world._nb_sparql_call += 1
    for l in self.world.graph.execute(self.sql, tuple(param.storid if hasattr(param, "storid") else param for param in params)):
      l2 = []
      i = 0
      while i < len(l):
        if self.column_types[i] == "objs":
          l2.append(self.world._to_python(l[i], None) or l[i])
          i += 1
        else:
          if l[i + 1] is None:
            l2.append(self.world._to_python(l[i], None) or l[i])
          else:
            l2.append(self.world._to_python(l[i], l[i + 1]))
          i += 2
      yield l2
      
    
class Column(object):
  def __init__(self, var, type = None, binding = None, name = None):
    self.var         = var
    self.type        = type
    self.binding     = binding
    self.name        = name
    
class Variable(object):
  def __init__(self, name):
    self.name           = name
    self.type           = "quads"
    self.fixed_datatype = None
    self.prop_type      = "quads" # Type when the variable is used as a property
    self.bindings       = []
    self.bind           = None
    
  def __repr__(self): return """<Variable %s type %s, %s bindings>""" % (self.name, self.type, len(self.bindings))
  
  def update_type(self, type):
    #print("UPDATE TYPE", self, "=>", type)
    if   self.type == "quads": self.type = type
    elif (type != self.type) and (type != "quads") :
      raise ValueError("Variable %s cannot be both %s and %s!" % (self.name, self.type, type))
    
class Table(object):
  def __init__(self, name, type = "quads"):
    self.name = name
    self.type = type
    
  def sql(self): return """%s %s""" % (self.type, self.name)

  
class SQLQuery(FuncSupport):
  def __init__(self, name):
    self.name                    = name
    self.preliminary             = False
    self.recursive               = False
    self.translator              = CURRENT_TRANSLATOR.get()
    self.distinct                = False
    self.raw_selects             = None
    self.tables                  = []
    self.name_2_table            = {}
    self.columns                 = []
    self.conditions              = []
    self.parameters              = []
    self.triples                 = []
    self.vars_needed_for_select  = set()
    self.vars                    = {}
    self.extra_sql               = ""
    self.select_simple_union     = False
  
  def __repr__(self): return "<%s '%s'>" % (self.__class__.__name__, self.sql())
  
  def sql(self):
    if self.tables:
      sql = """SELECT """
      if self.distinct: sql += "DISTINCT "
      sql += """%s FROM %s""" % (", ".join(str(column.binding) for column in self.columns), ", ".join(table.sql() for table in self.tables))
      if self.conditions:
        sql += """ WHERE %s""" % (" AND ".join(self.conditions))
    else:
      if self.select_simple_union:
        for i, column in enumerate(self.columns):
          if isinstance(column.binding, list): break
        l = []
        for j in range(len(self.columns[i].binding)):
          l.append([])
          for k, column in enumerate(self.columns):
            if k == i: l[-1].append(column.binding[j])
            else:      l[-1].append(column.binding)
        sql = """VALUES %s""" % ",".join("(%s)" % ",".join(str(k) for k in j) for j in l)
      else:
        sql = """VALUES (%s)""" % (",".join(str(column.binding) for column in self.columns))
        
    if self.extra_sql: sql += " %s" % self.extra_sql
    if self.preliminary: return """%s(%s) AS (%s)""" % (self.name, ", ".join(column.name for column in self.columns), sql)
    return sql
    
  def set_column_names(self, names):
    for column, name in zip(self.columns, names): column.name = name
    
  def parse_distinct(self, distinct):
    if isinstance(distinct, rply.Token): self.distinct = distinct and (distinct.value.upper() == "DISTINCT")
    else:                                self.distinct = distinct
    
  def parse_var(self, x):
    if isinstance(x, rply.Token): name = x.value
    else:                         name = x
    var = self.vars.get(name)
    if not var:
      self.vars[name] = var = Variable(name)
      #if self.raw_selects == "*": self.vars_needed_for_select.add(var)
    return var
  
  def parse_selects(self, selects):
    if selects is None:
      self.raw_selects = "*"
    else:
      self.raw_selects = selects
      vars_needed_for_select = { self.parse_var(select) for select in selects if (isinstance(select, rply.Token) and (select.name == "VAR")) or (isinstance(select, str)) }
      for var in vars_needed_for_select:
        self.expand_referenced_vars(var, self.vars_needed_for_select)
        
  def expand_referenced_vars(self, var, r):
    r.add(var)
    if var.bind:
      for var_name in var.bind.referenced_var_names:
        self.expand_referenced_vars(self.parse_var(var_name), r)
        
  def prepare_bind(self, bind):
    var      = self.parse_var(bind.var)
    var.bind = bind
    
  def parse_bind(self, bind):
    var      = self.parse_var(bind.var)
    var.bind = bind
    var.bindings.insert(0, self.parse_expression(bind.expression))
    
    fixed_type, fixed_datatype = self.infer_expression_type(bind.expression)
    if fixed_type is None: fixed_type = "quads"
    var.update_type(fixed_type)
    if fixed_type != "objs":  var.fixed_datatype = fixed_datatype
    
    #print("PARSE BIND", var.name, "=>", var.bindings[0], "TYPE", var.fixed_datatype)
    
  def parse_filter(self, filter):
    sql = self.parse_expression(filter.constraint)
    self.conditions.append(sql)
    
  def add_subqueries(self, sub):
    table = Table("p%s" % (len(self.tables) + 1), sub.name)
    self.tables.append(table)
    self.name_2_table[table.name] = table
    for column in sub.columns:
      var = self.parse_var(column.var)
      var.update_type(column.type)
      if not column.name.endswith("d"):
        self.create_conditions(self.conditions, table, column.name, var)
        
  def parse_triples(self, triples):
    if self.triples: raise ValueError("Cannot parse triples twice!")
    self.block = triples
    self.triples.extend(triples)
    
    if self.raw_selects is None: raise ValueError("Need to call parse_selects() before finalizing triples!")
    
    if self.raw_selects == "*":
      self.vars_needed_for_select = { self.parse_var(var_name) for var_name in self.block.get_ordered_vars() }
      
    for i, triple in enumerate(self.triples): # Pass 0: Inner blocks
      if isinstance(triple, Block):
        if isinstance(triple, SimpleTripleBlock) and len(triple) == 0: continue # Empty
        if isinstance(triple, UnionBlock) and triple.simple_union_triples:
          self.triples[i:i+1] = triple.simple_union_triples
          continue
        
        sub = self.translator.new_sql_query(None, triple, preliminary = True)
        self.add_subqueries(sub)
        
    for triple in list(self.triples): # Pass 1: Determine var type and prop type
      if isinstance(triple, Bind) or isinstance(triple, Filter) or isinstance(triple, Block): continue
      #if isinstance(triple, Bind):
      #  self.prepare_bind(triple)
      #  continue
      #if isinstance(triple, Filter): continue
      s, p, o = triple
      #if isinstance(self, SQLRecursivePreliminaryQuery): print("PRELIM PARSE TRIPLE", triple)
      #else:                                              print("MAIN   PARSE TRIPLE", triple)
      
      triple.local_table_type = triple.table_type
      if s.name == "VAR":
        var = self.parse_var(s)
        var.update_type("objs")
        if (p.name == "IRI") and (p.storid == rdfs_subpropertyof) and (o.name == "IRI"):
          parent_prop = self.translator.world._get_by_storid(o.storid)
          if   isinstance(parent_prop, ObjectPropertyClass): var.prop_type = "objs"
          elif isinstance(parent_prop, DataPropertyClass):   var.prop_type = "datas"
      if p.name == "VAR": self.parse_var(p).update_type("objs")
      if o.name == "VAR": self.parse_var(o).update_type(triple.local_table_type)
      
    for triple in list(self.triples): # Pass 2: Determine var type, which may be changed due to prop type
      if isinstance(triple, Bind) or isinstance(triple, Filter) or isinstance(triple, Block): continue
      s, p, o = triple
      if (triple.local_table_type == "quads") and (o.name == "VAR"): triple.local_table_type = self.parse_var(o).type
      if (triple.local_table_type == "quads") and (p.name == "VAR"): triple.local_table_type = self.parse_var(p).prop_type # Repeat (table.type == "quads") condition, since table.type may have been changed by the previous if block
      if o.name == "VAR": self.parse_var(o).update_type(triple.local_table_type)
      
    non_preliminary_triples = []
    for triple in list(self.triples): # Pass 3: Create recursive preliminary select
      if isinstance(triple, Bind) or isinstance(triple, Filter) or isinstance(triple, Block): continue
      s, p, o = triple
      triple.consider_s = triple.consider_p = triple.consider_o = True
      
      if p.modifier:
        if   (s.name != "VAR"): fixed = "s"
        elif (o.name != "VAR"): fixed = "o"
        else:
          nb_s = nb_o = 0
          for triple in self.triples:
            for x in triple.var_names:
              if x == s.value: nb_s += 1
              if x == o.value: nb_o += 1
          if   nb_s == 1:    fixed = "o"
          elif nb_o == 1:    fixed = "s"
          elif nb_s <= nb_o: fixed = "s"
          else:              fixed = "o"
        non_fixed = "o" if fixed == "s" else "s"
        
        vars = []
        if   (s.name == "VAR") and (fixed == "s"): fixed_var = s
        elif (o.name == "VAR") and (fixed == "o"): fixed_var = o
        else:                                      fixed_var = None
        if fixed_var: vars.append(self.parse_var(fixed_var))
        if  p.name == "VAR": vars.append(self.parse_var(p))
        
        prelim_triples = self.extract_triples(self.triples, vars, triple)
        #print("ZZZ", fixed, vars, prelim_triples)

        prelim = self.translator.get_recursive_preliminary_select(triple, fixed, fixed_var, prelim_triples)
        triple.local_table_type = prelim.name
        triple.consider_p = False
        if not(fixed_var and prelim_triples):
          if fixed == "s": triple.consider_s = False
          else:            triple.consider_o = False
          
      else:
        non_preliminary_triples.append(triple)
        
    selected_non_preliminary_triples = frozenset(self.extract_triples(non_preliminary_triples, self.vars_needed_for_select))
    
    for triple in self.triples: # Pass 4: create triples tables and conditions
      if    isinstance(triple, Bind):   self.parse_bind(triple);   continue
      elif  isinstance(triple, Filter): self.parse_filter(triple); continue
      elif  isinstance(triple, Block):  continue
      
      s, p, o = triple
      if (not p.modifier) and (not triple in selected_non_preliminary_triples): continue
      
      table = Table("q%s" % (len(self.tables) + 1), triple.local_table_type)
      #if (table.type == "quads") and (o.name == "VAR"): table.type = self.parse_var(o).type
      #if (table.type == "quads") and (p.name == "VAR"): table.type = self.parse_var(p).prop_type # Repeat (table.type == "quads") condition, since table.type may have been changed by the previous if block
      self.tables.append(table)
      self.name_2_table[table.name] = table
      
      if triple.consider_s: self.create_conditions(self.conditions, table, "s", s)
      if triple.consider_p: self.create_conditions(self.conditions, table, "p", p)
      if triple.consider_o: self.create_conditions(self.conditions, table, "o", o)
      
      if p.modifier == "+": self.conditions.append("%s.nb>0"  % table.name)
      
      
  def extract_triples(self, triples, vars, except_triple = None):
    var_names = { var.name for var in vars }
    while True:
      r = [triple for triple in triples if (not triple == except_triple) and isinstance(triple, Triple) and (not triple.var_names.isdisjoint(var_names))]
      var_names2 = { var_name for triple in r for var_name in triple.var_names }
      if var_names2 == var_names: return r
      var_names = var_names2
      
  def create_conditions(self, conditions, table, n, x):
    if isinstance(x, SpecialCondition):
      x.create_conditions(conditions, table, n)
    else:
      sql, sql_type, sql_d, sql_d_type = self._to_sql(x)
      if not sql   is None: conditions.append("%s.%s=%s" % (table.name, n, sql))
      if not sql_d is None: conditions.append("%s.d=%s"  % (table.name,    sql_d)) # Datatype part
      
      if x.name == "VAR": x = self.vars[x.value]
      if   isinstance(x, Variable):
        x.bindings.append("%s.%s" % (table.name, n))
      elif sql == "?":
        self.parameters.append(x.number)
        
  def finalize_columns(self):
    selected_parameter_index = 0
    i = 0
    if self.raw_selects == "*": selects = [self.vars[var] for var in self.block.get_ordered_vars() if not var.startswith("??")]
    else:                       selects = self.raw_selects

    def do_select(select):
      nonlocal selected_parameter_index
      if isinstance(select, str) and select.startswith("?"): select = self.vars[select]
      sql, sql_type, sql_d, sql_d_type = self._to_sql(select)
      
      if   isinstance(select, rply.Token) and (select.name == "VAR"): var_name = select.value
      elif isinstance(select, Variable):                              var_name = select.name
      else:                                                           var_name = None
      
      if sql == "?":
        self.parameters.insert(selected_parameter_index, select.number)
        selected_parameter_index += 1

      return var_name, sql, sql_type, sql_d, sql_d_type
    
    for select in selects:
      i += 1
      if isinstance(select, SimpleUnion):
        self.select_simple_union = True
        sql = []
        for select_item in select.items:
          var_name, sql_i, sql_type, sql_d, sql_d_type = do_select(select_item)
          sql.append(sql_i)
        sql_d = None # SimpleUnion is only supported for object here
        
      else:
        var_name, sql, sql_type, sql_d, sql_d_type = do_select(select)
        
      if not sql   is None: self.columns.append(Column(var_name, sql_type,   sql,   "col%s_o" % i))
      if not sql_d is None: self.columns.append(Column(var_name, sql_d_type, sql_d, "col%s_d" % i))
        
  def _to_sql(self, x):
    if isinstance(x, rply.Token) and (x.name == "VAR"): x = self.parse_var(x)
    
    if   isinstance(x, str): return x, "value", None, None
    elif isinstance(x, Variable):
      if not x.bindings: return None, None, None, None
      binding = x.bindings[0]
      
      if   x.type == "objs":  return binding, "objs", None, None
      else:
        if not x.fixed_datatype is None:
          if isinstance(x.fixed_datatype, Variable):
            dropit, dropit, other_sql_d, other_sql_d_type = self._to_sql(x.fixed_datatype)
            return binding, "datas", other_sql_d, other_sql_d_type
          else:
            return binding, "datas", x.fixed_datatype, "datas"
        type = "datas" if x.type == "datas" else "quads"
        return binding, type, "%sd" % binding[:-1], type
    elif x.name == "IRI": return x.storid, "objs", None, None
    elif x.name == "ARG": return "?", "objs", None, None # XXX data parameter
    else:
      if   x.name == "DATA":            return x.value, "value", x.datatype, "value"
      elif isinstance(x.value, locstr): return x.value, "value", "'@%s'" % x.value.lang, "value"
      else:                             return x.value, "value", None, None
      
    
class SQLCompoundQuery(object):
  recursive = False
  def __init__(self, name):
    self.name                    = name
    self.translator              = CURRENT_TRANSLATOR.get()
    self.queries                 = []
    self.preliminary             = False
    
  def __repr__(self): return "<%s '%s'>" % (self.__class__.__name__, self.sql())

  def append(self, query, operator = ""):
    query.operator = operator
    self.queries.append(query)
    
  def sql(self):
    sql = ""
    for i, query in enumerate(self.queries):
      if i != 0: sql += "\n%s\n" % query.operator
      sql += query.sql()
    if self.preliminary: return """%s(%s) AS (%s)""" % (self.name, ", ".join(column.name for column in self.columns), sql)
    return sql

  def finalize_compounds(self):
    has_d = set()
    for query in self.queries:
      for column in query.columns:
        if column.name.endswith("d"):
          has_d.add(column.name.split("_", 1)[0])
          
    for query in self.queries:
      for i, column in enumerate(query.columns):
        if column is query.columns[-1]: continue
        if column.name.endswith("o") and (column.name.split("_", 1)[0] in has_d):
          column.type = "quads"
          if not query.columns[i+1].name.endswith("d"):
            query.columns.insert(i + 1, Column(column.var_name, "quads", "NULL", "%sd" % column.name[:-1]))
            
            
class SQLRecursivePreliminaryQuery(SQLQuery):
  def __init__(self, name, triple, fixed, fixed_var):
    s, p, o = triple
    translator = CURRENT_TRANSLATOR.get()
    self.fixed        = fixed
    self.fixed_var    = fixed_var
    self.non_fixed    = "o" if fixed == "s" else "s"
    
    if isinstance(p, NegatedPropSetPath): self.need_d = True
    else:                                 self.need_d = (p.modifier == "?") and not isinstance(triple.Prop, ObjectPropertyClass)
    
    self.need_orig    = not self.fixed_var is None # XXX Optimizable
    self.need_nb      =  p.modifier != "*"
    SQLQuery.__init__(self, "%s_%s" % (name, "quads" if self.need_d else "objs"))
    self.recursive    = True
    self.preliminary  = True
    
  def build(self, triple, prelim_triples):
    s, p, o = triple
    column_names = [self.non_fixed] + ["d"] * self.need_d + [self.fixed] * self.need_orig + ["nb"] * self.need_nb
    if self.fixed_var and prelim_triples: value = self.fixed_var
    else:                                 value = s if self.fixed == "s" else o
    self.parse_selects([value] + ["NULL"] * self.need_d + [value] * self.need_orig + ["0"] * self.need_nb)
    self.parse_triples(prelim_triples)
    self.finalize_columns()
    self.set_column_names(column_names)
    
    p_conditions = []
    self.create_conditions(p_conditions, Table("q", "quads" if self.need_d else "objs"), "p", p)
    self.extra_sql = """
UNION
SELECT q.%s%s%s%s FROM %s q, %s rec WHERE %s %sAND q.%s=rec.%s""" % (
  self.non_fixed,
  ", q.d"                 if self.need_d    else "",
  ", rec.%s" % self.fixed if self.need_orig else "",
  ", rec.nb+1"            if self.need_nb   else "",
  "quads"                 if self.need_d    else "objs",
  self.name, " AND ".join(p_conditions),
  "AND rec.nb=0 " if p.modifier == "?" else "",
  self.fixed, self.non_fixed)
  
  
  
if __name__ == '__main__':
  onto = get_ontology("http://test.org/onto.owl#")
  
  with onto:
    class A(Thing): pass
    class A1(A): pass
    class A11(A1): pass
    class A2(A): pass
    class B(Thing): pass
    class C(Thing): pass
    
    class price(Thing >> float): label = ["price"]
    class price_vat_free(price): pass
    class annot(AnnotationProperty): pass
    
    A .label.append("Classe A")
    A1.label.append("Classe A1")
    
    a1 = A(label = [locstr("label_a", "en")])
    b1 = B(label = [locstr("label_b", "en")])
    b2 = B(label = [locstr("label_b", "en")])
    b3 = B(label = [locstr("label_b", "fr")])
    
    a1.price = [10.1, 20.4, 5.3]
    a1.price_vat_free = [8.0]
    a1.annot = [8.0, "eee", locstr("xxx", "fr")]
    
  s = """
SELECT  ?x  {
   { ?x a onto:B . }
   UNION
   { ?x rdfs:subClassOf onto:A . }
 }
"""
  
  import owlready2, time
  t0 = time.time()
  p = Translator(owlready2.default_world)
  q = p.parse(s)
  print()
  print()
  print(s)
  print()
  print()
  print("prepared in %s s" % (time.time() - t0))
  
  print()
  print()
  print(q.sql)
  print()
  print()
  
  t0 = time.time()
  r = list(q.execute())
  print("executed in %s s" % (time.time() - t0))
  print()
  
  for l in r: print(l)
  
  
  if 0: # RDFlib
    l = list(default_world.sparql_query(s))
    t0 = time.time()
    l = list(default_world.sparql_query(s))
    print("executed in %s s" % (time.time() - t0))
    for l in r: print(l)

  
