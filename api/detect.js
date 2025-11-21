# Vercel Serverless Function for AI Text Detection with Gemini
# Save this as: api/detect.js

import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

export default async function handler(req, res) {
  // Enable CORS for all origins
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET,OPTIONS,PATCH,DELETE,POST,PUT"
  );
  res.setHeader(
    "Access-Control-Allow-Headers",
    "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version"
  );

  if (req.method === "OPTIONS") {
    res.status(200).end();
    return;
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    const { text } = req.body;

    if (!text || text.length < 10) {
      return res
        .status(400)
        .json({ error: "Text must be at least 10 characters" });
    }

    if (!process.env.GEMINI_API_KEY) {
      return res
        .status(500)
        .json({ error: "Gemini API key not configured" });
    }

    const model = genAI.getGenerativeModel({ model: "gemini-pro" });

    const prompt = `You are an expert AI text detector. Analyze the following text and determine if it was written by AI or a human.

Provide a detailed analysis in JSON format with exactly these fields:
1. aiProbability (0-100): Percentage likelihood the text was AI-generated
2. humanProbability (0-100): Percentage likelihood the text was written by a human
3. confidence ("High" or "Medium" or "Low"): Your confidence in the assessment
4. isAI (true/false): Whether you believe the text is AI-generated
5. indicators (array of strings): Key indicators that led to your conclusion
6. styleAnalysis (string): Detailed writing style analysis

Text to analyze:
"${text}"

Respond ONLY with valid JSON, no other text or markdown:`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const analysisText = response.text();

    // Parse JSON response
    let analysis;
    try {
      // Try to extract JSON from response
      const jsonMatch = analysisText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        analysis = JSON.parse(jsonMatch[0]);
      } else {
        analysis = JSON.parse(analysisText);
      }
    } catch (e) {
      console.error("Failed to parse Gemini response:", analysisText);
      return res.status(500).json({
        error: "Failed to parse AI analysis",
        debug: analysisText.substring(0, 200),
      });
    }

    // Validate response structure
    if (!analysis || typeof analysis !== "object") {
      return res.status(500).json({ error: "Invalid AI response format" });
    }

    // Ensure all required fields exist
    const validatedAnalysis = {
      aiProbability: Math.min(100, Math.max(0, analysis.aiProbability || 0)),
      humanProbability: Math.min(
        100,
        Math.max(0, analysis.humanProbability || 0)
      ),
      confidence: ["High", "Medium", "Low"].includes(analysis.confidence)
        ? analysis.confidence
        : "Medium",
      isAI: Boolean(analysis.isAI),
      indicators: Array.isArray(analysis.indicators)
        ? analysis.indicators.slice(0, 5)
        : [],
      styleAnalysis: String(analysis.styleAnalysis || "No analysis provided"),
    };

    return res.status(200).json({
      success: true,
      ...validatedAnalysis,
      wordCount: text.split(/\s+/).length,
      analysisTimestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error("API Error:", error);
    return res.status(500).json({
      error: "Failed to analyze text",
      message: error.message,
      success: false,
    });
  }
}