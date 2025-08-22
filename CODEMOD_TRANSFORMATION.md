# Codemod Transformation Summary

## Transformation Applied
Apply codemod transformation

## Pattern Generated
```grit
engine marzano(0.1)
language python

pattern update_share_calculation() {
  file($body) where {
    $body <: contains class_definition(name="AloYogaAggregatedShareSelection", body=$class_body) where {
        $class_body <: contains `def select_aggregated_shares(self, scope_dict: dict) -> dict:
    $func_body` => `def select_aggregated_shares(self, scope_dict: Dict[str, DataFrame], share_list_config: List[Dict]) -> dict:
    $new_func_body` where {
            $new_func_body = $func_body,
            $new_func_body <: contains `self.share_list_config` => `share_list_config`,
            add_import(source="typing", name="Dict"),
            add_import(source="typing", name="List"),
            add_import(source="pyspark.sql", name="DataFrame")
        },
        $class_body <: maybe contains function_definition(name="main", body=$main_body) where {
            $main_body <: contains `self.select_aggregated_shares(scope_dict=$scope)` => `self.select_aggregated_shares(scope_dict=$scope, share_list_config=self.share_list_config)`
        },
        $class_body <: maybe contains function_definition(name="run", body=$run_body) where {
            $run_body <: contains `self.select_aggregated_shares(scope_dict=$scope)` => `self.main($scope)`
        }
    }
  }
}

sequential {
  maybe contains update_share_calculation()
}
```

No files were transformed. The pattern may not match any code in the
repository, or the transformation may not result in any changes.

This pattern was generated automatically by the codemod tool.
