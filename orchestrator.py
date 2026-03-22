import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

AGENTS = {
    "A": """あなたはTwitter調査係です。
化粧品・美容関連のトレンドワード、口コミ、ハッシュタグを調査・分析してください。
数値・具体例を含めて報告し、推測は「要確認」と明記してください。""",

    "B": """あなたはInstagram調査係です。
美容・化粧品関連の人気ハッシュタグ、インフルエンサー、競合ブランドの戦略を調査してください。
数値・具体例を含めて報告し、推測は「要確認」と明記してください。""",

    "C": """あなたは市場調査係です。
化粧品市場の規模・動向・競合分析・消費者動向を調査してください。
数値・出典を明記し、推測は「要確認」と明記してください。""",

    "D": """あなたはマーケティング係です。
以下の調査結果を踏まえて、具体的なマーケティング戦略を立案してください。
短期・中期・長期の施策に分けて、実行可能なアクションプランを提案してください。""",

    "E": """あなたは否定係です。
提案された戦略の弱点・リスク・矛盾を徹底的に指摘してください。
消費者視点・競合視点・コスト視点から批判的に分析し、何が足りないかも明示してください。""",

    "F": """あなたは改善提案係です。
否定係の指摘を全て反映した改善版の提案をまとめてください。
中村さんが即座に動けるレベルまで具体化してください。"""
}

def run_agent(agent_name, system_prompt, user_message):
    """1人のエージェントを独立して実行する"""
    print(f"\n{'='*50}")
    print(f"エージェント {agent_name} 作業中...")
    print(f"{'='*50}")
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    result = response.content[0].text
    print(result)
    return result

def run_orchestrator(theme):
    """A→B→C→D→E→F の順で全エージェントを実行"""
    
    print(f"\n🎯 テーマ：{theme}")
    print("オーケストレーター起動：A→B→C→D→E→F の順で実行します\n")
    
    results = {}
    
    # A: Twitter調査
    results["A"] = run_agent("A（Twitter調査）", 
                              AGENTS["A"], 
                              f"テーマ：{theme}\nTwitterでの調査結果を報告してください。")
    
    # B: Instagram調査
    results["B"] = run_agent("B（Instagram調査）", 
                              AGENTS["B"], 
                              f"テーマ：{theme}\nInstagramでの調査結果を報告してください。")
    
    # C: 市場調査
    results["C"] = run_agent("C（市場調査）", 
                              AGENTS["C"], 
                              f"テーマ：{theme}\n市場調査結果を報告してください。")
    
    # D: 戦略立案（A・B・Cの結果を渡す）
    d_input = f"""テーマ：{theme}

【Twitter調査結果（A）】
{results['A']}

【Instagram調査結果（B）】
{results['B']}

【市場調査結果（C）】
{results['C']}

上記の調査結果を踏まえてマーケティング戦略を立案してください。"""
    
    results["D"] = run_agent("D（マーケティング戦略）", AGENTS["D"], d_input)
    
    # E: 否定・批判（Dの結果を渡す）
    e_input = f"""以下のマーケティング戦略の問題点を指摘してください。

【戦略提案（D）】
{results['D']}"""
    
    results["E"] = run_agent("E（否定・批判）", AGENTS["E"], e_input)
    
    # F: 改善提案（D・Eの結果を渡す）
    f_input = f"""以下の戦略と批判を踏まえて、改善版をまとめてください。

【マーケティング戦略（D）】
{results['D']}

【批判・問題点（E）】
{results['E']}"""
    
    results["F"] = run_agent("F（改善提案）", AGENTS["F"], f_input)
    
    print("\n" + "="*50)
    print("✅ 全エージェント完了。中村さんに確認を取ってから納品します。")
    print("="*50)
    
    return results

# 実行例
if __name__ == "__main__":
    theme = "30代向けスキンケアシリーズの新商品ローンチ"
    run_orchestrator(theme)
