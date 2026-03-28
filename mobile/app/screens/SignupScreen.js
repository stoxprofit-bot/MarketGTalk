import React, { useState } from "react";
import { Alert, Text } from "react-native";

import { Button, Card, Heading, Input, Label } from "../components/UI";
import { Screen } from "../components/Screen";
import { useAuth } from "../context/AuthContext";

export function SignupScreen({ navigation }) {
  const { authenticate } = useAuth();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = async () => {
    try {
      await authenticate("signup", { full_name: fullName, email, password });
    } catch (error) {
      Alert.alert("Signup failed", error.message);
    }
  };

  return (
    <Screen>
      <Heading>Create account</Heading>
      <Card>
        <Label>Full name</Label>
        <Input value={fullName} onChangeText={setFullName} />
        <Label>Email</Label>
        <Input value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
        <Label>Password</Label>
        <Input value={password} onChangeText={setPassword} secureTextEntry />
        <Button title="Sign up" onPress={onSubmit} />
        <Text onPress={() => navigation.navigate("Login")} style={{ color: "#173a63", textAlign: "center" }}>
          Already have an account? Login
        </Text>
      </Card>
    </Screen>
  );
}
