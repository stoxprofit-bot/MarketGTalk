import React, { useEffect, useState } from "react";
import { Alert, Text } from "react-native";

import { api } from "../api/client";
import { Screen } from "../components/Screen";
import { Card, Heading } from "../components/UI";
import { useAuth } from "../context/AuthContext";

export function TradesScreen() {
  const { token } = useAuth();
  const [trades, setTrades] = useState([]);

  useEffect(() => {
    api.trades(token).then(setTrades).catch((error) => Alert.alert("Could not load trades", error.message));
  }, []);

  return (
    <Screen>
      <Heading>Recent Trades</Heading>
      {trades.map((trade) => (
        <Card key={trade.id}>
          <Text style={{ fontWeight: "700", color: "#173a63" }}>
            {trade.side.toUpperCase()} {trade.symbol}
          </Text>
          <Text>Status: {trade.status}</Text>
          <Text>Exchange: {trade.exchange}</Text>
          <Text>Quantity: {trade.quantity}</Text>
          <Text>Price: {trade.price}</Text>
          {trade.error ? <Text>Error: {trade.error}</Text> : null}
        </Card>
      ))}
    </Screen>
  );
}
