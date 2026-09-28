from pyspark.sql import DataFrame
from pyspark.sql import functions as F

EARTH_RADIUS_KM = 6371.0088

def add_training_features(df: DataFrame) -> DataFrame:
    features_df = (
        df
        .withColumn("transaction_hour", F.hour("trans_date_trans_time"))
        .withColumn("transaction_day", F.dayofmonth("trans_date_trans_time"))
        .withColumn("day_of_week", F.dayofweek("trans_date_trans_time"))
        .withColumn("transaction_month", F.month("trans_date_trans_time"))
        .withColumn(
            "is_weekend",
            F.when(F.dayofweek("trans_date_trans_time").isin(1, 7), 1).otherwise(0)
        )
        .withColumn(
            "customer_age",
            F.floor(
                F.months_between(
                    F.to_date("trans_date_trans_time"),
                    F.col("dob")
                ) / 12
            )
        )
        .withColumn("log_amount", F.log1p(F.col("amt")))
        .withColumn("log_city_pop", F.log1p(F.col("city_pop")))
    )

    customer_lat = F.radians(F.col("lat"))
    customer_long = F.radians(F.col("long"))
    merchant_lat = F.radians(F.col("merch_lat"))
    merchant_long = F.radians(F.col("merch_long"))

    delta_lat = merchant_lat - customer_lat
    delta_long = merchant_long - customer_long

    a = (
        F.pow(F.sin(delta_lat / 2), 2)
        + F.cos(customer_lat)
        * F.cos(merchant_lat)
        * F.pow(F.sin(delta_long / 2), 2)
    )

    return features_df.withColumn(
        "distance_km",
        2 * F.lit(EARTH_RADIUS_KM) * F.asin(F.sqrt(a))
    )
