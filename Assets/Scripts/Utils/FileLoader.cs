using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Globalization;
using Newtonsoft.Json;

public static class FileLoader
{
    public static float[][] LoadEulerAngles(string filePath)
    {
        string[] lines = File.ReadAllLines(filePath);
        float[][] angles = new float[lines.Length][];
        for (int i = 0; i < lines.Length; i++)
        {
            string[] line = lines[i].Split(',');
            angles[i] = new float[line.Length];
            for (int j = 0; j < line.Length; j++)
            {
                angles[i][j] = float.Parse(line[j], CultureInfo.InvariantCulture);
            }
        }
        return angles;
    }

    public static float[,] LoadQuaternionAngles(string filePath)
    {
        string[] lines = File.ReadAllLines(filePath);
        int rows = lines.Length;
        int cols = lines[0].Split(',').Length;
        float[,] angles = new float[rows, cols];

        for (int i = 0; i < rows; i++)
        {
            string[] line = lines[i].Split(',');
            for (int j = 0; j < cols; j++)
            {
                angles[i, j] = float.Parse(line[j]);
            }
        }
        return angles;
    }

    public static Dictionary<string, object> LoadJson(string filePath)
    {
        if (!File.Exists(filePath))
        {
            Debug.LogError("JSON file not found: " + filePath);
            return null;
        }

        string jsonText = File.ReadAllText(filePath);
        Dictionary<string, object> jsonData = JsonConvert.DeserializeObject<Dictionary<string, object>>(jsonText);

        return jsonData;
    }
}
