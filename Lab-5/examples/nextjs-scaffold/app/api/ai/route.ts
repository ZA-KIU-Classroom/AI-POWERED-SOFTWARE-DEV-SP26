import { NextRequest, NextResponse } from "next/server";
import { callModel } from "@/lib/llm-service";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { prompt, system, model } = body as {
      prompt:  string;
      system?: string;
      model?:  string;
    };

    if (!prompt || typeof prompt !== "string") {
      return NextResponse.json(
        { error: "prompt is required and must be a string" },
        { status: 400 }
      );
    }

    const result = await callModel({
      prompt,
      system:  system  ?? "You are a helpful assistant.",
      model:   model   ?? process.env.DEFAULT_MODEL ?? "google/gemini-2.5-flash",
      purpose: "api_generate",
    });

    return NextResponse.json(result);
  } catch (err) {
    console.error("[AI route error]", err);
    return NextResponse.json(
      { error: "Model call failed", detail: String(err) },
      { status: 500 }
    );
  }
}
