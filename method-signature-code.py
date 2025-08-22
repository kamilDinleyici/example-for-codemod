from rocks.noob.share_calculation import AggregatedShareSelection
from pyspark.sql import functions as F


class AloYogaAggregatedShareSelection(AggregatedShareSelection):
    """
    Aggregated Share Selection for share calculation pipeline
    """

    def select_aggregated_shares(self, scope_dict: Dict[str, DataFrame], share_list_config: List[Dict]):
        """
        Joins the respective share table & selects for output level

        :param scope_dict: scope dictionary
        :type scope_dict: dict
        :return: dictionary of share dataframes
        :rtype: dict
        """
        output_level = self.conf.get("output_level")
        share_dict = {}
    
        for key, df in scope_dict.items():
            count = 0
            # loop over only for the respective key.
            for share_config in [
                share_config
                for share_config in share_list_config
                if share_config["share_level"] == key
            ]:
                key_cols = share_config["forecast_level"]
                share_df = self.get_share_table(share_config)
                df = df.join(share_df, on=key_cols, how="left")
                df = df.withColumnRenamed("share", f"share_{count}")
                count += 1
    
            share_expr = [f"share_{c}" for c in range(count)]
            # coalesce all the prejoined shares on hierarchy level.
            df = df.withColumn("selected_share", F.coalesce(*share_expr))
    
            if self.default_share_value is not None:
                self.log.info(
                    "Filling the null shares with default share value %s",
                    self.default_share_value,
                )
                df = df.fillna({"selected_share": self.default_share_value})
    
            primary_key = list(set([*output_level, key]))
            df = df.select(
                *primary_key,
                F.col("selected_share").cast("float").alias("selected_share"),
            )
    
            # thanks to InventDataFrame
            df = df.set_metadata(primary_key=primary_key)
    
            share_dict[key] = df
        return share_dict