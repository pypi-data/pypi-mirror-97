# Copyright IBM Corp. 2020. All Rights Reserved.


from typing import Optional, Tuple

from attr import attrs, evolve


@attrs(auto_attribs=True, frozen=True, kw_only=True)
class CpdScope:
    has_prefix: bool
    context: Optional[str]
    scope_type: str
    scope_id: str

    def __str__(self) -> str:
        result = f"{self.context}/{self.scope_type}/{self.scope_id}"
        if self.has_prefix:
            result = "cpd://" + result
        return result

    @classmethod
    def try_from_string(cls, s: str) -> Tuple[Optional['CpdScope'], str]:
        if s.startswith("cpd://") or s.startswith("/"):
            return cls._from_string_and_rest(s)
        else:
            return None, s

    @classmethod
    def from_string(cls, s: str) -> 'CpdScope':
        return cls._from_string_and_rest(s)[0]

    @classmethod
    def _from_string_and_rest(cls, s: str) -> Tuple['CpdScope', str]:
        has_prefix = False
        if s.startswith("cpd://"):
            has_prefix = True
            s = s[len("cpd://"):]

        parts = s.split("/")
        if len(parts) < 3:
            raise TypeError(f"Wrong format of CPD Scope: '{s}'")

        context = parts[0]
        scope_type = parts[1]
        scope_id = parts[2]
        other_parts = parts[3:]

        scope_types = [
            "projects",
            "spaces",
            "catalogs",
        ]
        if scope_type.find("?") != -1:
            raise TypeError(f"CPD Scope for CPD Orchestration must use id, not name or tags")
        if scope_type not in scope_types:
            raise TypeError(f"Unknown scope type: '{scope_type}'")

        return CpdScope(
            has_prefix = has_prefix,
            context = context,
            scope_type = scope_type,
            scope_id = scope_id,
        ), "/".join(other_parts)

@attrs(auto_attribs=True, frozen=True, kw_only=True)
class CpdPath:
    scope: Optional[CpdScope]
    path: str
    query: Optional[str] = None

    def __str__(self) -> str:
        result = []
        if self.scope is not None:
            result.append(str(self.scope))
        if self.path != '':
            result.append(self.path)
        result_str = "/".join(result)
        if self.query is not None:
            result_str += '?' + self.query
        return result_str

    @classmethod
    def from_string(cls, s: str) -> 'CpdPath':
        scope, s = CpdScope.try_from_string(s)

        # if no scope, an additional case of "just by-id asset" must be checked
        if scope is None:
            if s.find("/") == -1: # no slashes --- it is by-id asset
                s = f"assets/{s}"

        if s.count("?") > 1:
            raise TypeError("Question mark can only be used once.")

        try:
            qmark_idx = s.rindex("?")
            s, query = s[:qmark_idx-1], s[qmark_idx+1:]
        except ValueError:
            query = None

        path = CpdPath(scope = scope, path = s, query = query)
        return path

    def resource_id(self) -> Optional[str]:
        if self.query is not None:
            # if query is defined, cpd_path is not pointing at a specific
            # resource_id but instead, it searches using that query
            return None
        # otherwise, it's the last part of path
        return self.path.split('/')[-1]

    def is_relative(self) -> bool:
        return self.scope is None

    def resolve_at(self, cpd_scope: CpdScope) -> 'CpdPath':
        if self.scope is not None:
            return evolve(self)
        return evolve(self, scope=cpd_scope)
