import React, { useEffect, useState } from "react";
import { Alert, Text } from "react-native";

import { api } from "../api/client";
import { Screen } from "../components/Screen";
import { Button, Card, Heading, Input, Label } from "../components/UI";
import { useAuth } from "../context/AuthContext";

export function AdminScreen() {
  const { token } = useAuth();
  const [symbol, setSymbol] = useState("BTC/USDT");
  const [side, setSide] = useState("buy");
  const [price, setPrice] = useState("64000");
  const [quantity, setQuantity] = useState("0.002");
  const [exchange, setExchange] = useState("c2c1");
  const [history, setHistory] = useState([]);

  const loadHistory = () => {
    api.signalHistory(token).then(setHistory).catch(() => setHistory([]));
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const sendSignal = async () => {
    try {
      await api.createSignal(
        {
          symbol,
          side,
          price: Number(price),
          quantity: Number(quantity),
          exchange,
          order_type: "limit"
        },
        token
      );
      Alert.alert("Signal sent", "Copy trade broadcast completed");
      loadHistory();
    } catch (error) {
      Alert.alert("Signal failed", error.message);
    }
  };

  return (
    <Screen>
      <Heading>Admin Signals</Heading>
      <Card>
        <Label>Symbol</Label>
        <Input value={symbol} onChangeText={setSymbol} autoCapitalize="characters" />
        <Label>Side</Label>
        <Input value={side} onChangeText={setSide} autoCapitalize="none" />
        <Label>Limit price</Label>
        <Input value={price} onChangeText={setPrice} keyboardType="numeric" />
        <Label>Quantity</Label>
        <Input value={quantity} onChangeText={setQuantity} keyboardType="numeric" />
        <Label>Exchange</Label>
        <Input value={exchange} onChangeText={setExchange} autoCapitalize="none" />
        <Button title="Broadcast signal" onPress={sendSignal} />
      </Card>
      {history.map((signal) => (
        <Card key={signal.id}>
          <Text style={{ fontWeight: "700", color: "#173a63" }}>
            {signal.side.toUpperCase()} {signal.symbol}
          </Text>
          <Text>
            Qty {signal.quantity} @ {signal.price}
          </Text>
          <Text>
            Success {signal.success_count}/{signal.executed_users}
          </Text>
        </Card>
      ))}
    </Screen>
  );
}
