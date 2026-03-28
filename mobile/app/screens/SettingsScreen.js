import React, { useEffect, useState } from "react";
import { Alert, Text } from "react-native";

import { api } from "../api/client";
import { Screen } from "../components/Screen";
import { Button, Card, Heading, Input, Label } from "../components/UI";
import { useAuth } from "../context/AuthContext";

export function SettingsScreen() {
  const { token, user, setUser, logout } = useAuth();
  const [apiKey, setApiKey] = useState("");
  const [secretKey, setSecretKey] = useState("");
  const [exchange, setExchange] = useState("c2c1");
  const [riskLimit, setRiskLimit] = useState(String(user?.max_trade_size || 1000));
  const [status, setStatus] = useState(null);

  useEffect(() => {
    api.coinSwitchStatus(token).then(setStatus).catch(() => setStatus({ connected: false }));
  }, []);

  const connect = async () => {
    try {
      const result = await api.connectCoinSwitch({ api_key: apiKey, secret_key: secretKey, exchange }, token);
      setStatus(result);
      Alert.alert("Success", "CoinSwitch keys connected");
    } catch (error) {
      Alert.alert("Connection failed", error.message);
    }
  };

  const saveRiskLimit = async () => {
    try {
      const updatedUser = await api.updateRiskLimit(Number(riskLimit), token);
      setUser(updatedUser);
      Alert.alert("Saved", "Risk limit updated");
    } catch (error) {
      Alert.alert("Save failed", error.message);
    }
  };

  return (
    <Screen>
      <Heading>Settings</Heading>
      <Card>
        <Text style={{ color: "#173a63", fontWeight: "700" }}>CoinSwitch connection</Text>
        <Text>{status?.connected ? `Connected to ${status.exchange}` : "Not connected"}</Text>
        <Label>API key</Label>
        <Input value={apiKey} onChangeText={setApiKey} autoCapitalize="none" />
        <Label>Secret key</Label>
        <Input value={secretKey} onChangeText={setSecretKey} autoCapitalize="none" secureTextEntry />
        <Label>Exchange</Label>
        <Input value={exchange} onChangeText={setExchange} autoCapitalize="none" />
        <Button title="Connect CoinSwitch" onPress={connect} />
      </Card>
      <Card>
        <Text style={{ color: "#173a63", fontWeight: "700" }}>Risk management</Text>
        <Label>Max trade size in quote currency</Label>
        <Input value={riskLimit} onChangeText={setRiskLimit} keyboardType="numeric" />
        <Button title="Save risk limit" onPress={saveRiskLimit} />
      </Card>
      <Button title="Logout" onPress={logout} variant="secondary" />
    </Screen>
  );
}
