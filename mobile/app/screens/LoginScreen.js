import React, { useState } from "react";
import { Alert, Text } from "react-native";

import { Button, Card, Heading, Input, Label } from "../components/UI";
import { Screen } from "../components/Screen";
import { useAuth } from "../context/AuthContext";

export function LoginScreen({ navigation }) {
  const { authenticate } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = async () => {
    try {
      await authenticate("login", { email, password });
    } catch (error) {
      Alert.alert("Login failed", error.message);
    }
  };

  return (
    <Screen>
      <Heading>CopyTrade</Heading>
      <Card>
        <Label>Email</Label>
        <Input value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
        <Label>Password</Label>
        <Input value={password} onChangeText={setPassword} secureTextEntry />
        <Button title="Login" onPress={onSubmit} />
        <Text onPress={() => navigation.navigate("Signup")} style={{ color: "#173a63", textAlign: "center" }}>
          New here? Create an account
        </Text>
      </Card>
    </Screen>
  );
}
