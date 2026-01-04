import { Text, View, StyleSheet, Button, Image } from "react-native";
import { useState } from "react";
import * as ImagePicker from "expo-image-picker";
import { Audio } from "expo-av";

export default function App() {
  const [image, setImage] = useState(null);
  const [video, setVideo] = useState(null);
  const [recording, setRecording] = useState(null);
  const [result, setResult] = useState("No diagnosis yet");

  // CAMERA IMAGE
  const pickImage = async () => {
    await ImagePicker.requestCameraPermissionsAsync();
    const res = await ImagePicker.launchCameraAsync({ quality: 0.7 });
    if (!res.canceled) setImage(res.assets[0].uri);
  };

  // VIDEO
  const recordVideo = async () => {
    await ImagePicker.requestCameraPermissionsAsync();
    const res = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Videos,
      videoMaxDuration: 15
    });
    if (!res.canceled) setVideo(res.assets[0].uri);
  };

  // AUDIO
  const startRecording = async () => {
    await Audio.requestPermissionsAsync();
    const { recording } = await Audio.Recording.createAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY
    );
    setRecording(recording);
  };

  const stopRecording = async () => {
    await recording.stopAndUnloadAsync();
    setRecording(null);
  };

  // DIAGNOSIS
  const runDiagnosis = async () => {
    try {
      const response = await fetch("http://192.0.0.4:5000/api/diagnosis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          machine: "fan",
          inputs: {
            images: image ? 1 : 0,
            video: video ? true : false,
            audio: recording ? true : false
          }
        })
      });
      const data = await response.json();
      setResult(`${data.result} (${data.confidence})`);
    } catch {
      setResult("Backend error");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>AutoFix Reality</Text>

      <Button title="Open Camera (Image)" onPress={pickImage} />
      {image && <Image source={{ uri: image }} style={styles.image} />}

      <Button title="Record Video (3–15s)" onPress={recordVideo} />

      <Button
        title={recording ? "Stop Sound Recording" : "Record Sound"}
        onPress={recording ? stopRecording : startRecording}
      />

      <Button title="Run Diagnosis" onPress={runDiagnosis} />

      <Text style={styles.result}>{result}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#0f172a"
  },
  title: {
    fontSize: 26,
    color: "#38bdf8",
    marginBottom: 20
  },
  image: {
    width: 200,
    height: 200,
    marginVertical: 15,
    borderRadius: 10
  },
  result: {
    color: "#e5e7eb",
    marginTop: 15,
    fontSize: 16
  }
});
