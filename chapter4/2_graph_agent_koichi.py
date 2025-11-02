# import asyncio
# import boto3
# import operator
import os
from typing import Annotated, Literal, Dict, Any

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# web_search = TavilySearch(max_results=2)

# ステートの定義
class State(TypedDict):
    query: str
    search_result: str
    summary: str

graph = StateGraph(State)

# ノード関数の定義
def template_node(state: State) -> dict:
    print("天気予報サービスをご利用ください")
    return {}

def web_search_node(state: State) -> dict:
    query = state["query"]
    # TODO: 実際の検索API呼び出し
    result = f"「{query}」の検索結果: ダミーテキスト..."
    return {"search_result": result}

def summarize_node(state: State) -> dict:
    search_result = state["search_result"]
    # TODO: 生成AIによるサマライズ
    result = f"「{search_result}」の要約結果： ダミーテキスト..."
    return {"summary": result}

def sns_node(state: State) -> dict:
    summary = state["summary"]
    # topic_arn = os.getenv("SNS_TOPIC_ARN")
    # sns_client = boto3.client('sns')
    # sns_client.publish(TopicArn=topic_arn, Message=summary)
    return {}

# ルーティング関数の定義
def routing_function(state: State) -> Literal["template_node", "web_search_node"]:
    if "天気" in state["query"]:
        return "template_node"
    else:
        return "web_search_node"

# ノードの定義
graph.add_node("template_node", template_node)
graph.add_node("web_search_node", web_search_node)
graph.add_node("summarize_node", summarize_node)
graph.add_node("sns_node", sns_node)

# エッジの定義
graph.add_conditional_edges(START, routing_function)
graph.add_edge("template_node", END)
graph.add_edge("web_search_node", "summarize_node")
graph.add_edge("summarize_node", "sns_node")
graph.add_edge("sns_node", END)

# グラフのコンパイル
app = graph.compile()

# 実行
# response = app.invoke({"query": "今日を教えてください"})
# print(response)


from IPython.display import Image, display

# display(Image(app.get_graph().draw_mermaid_png()))
png_bytes = app.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_bytes)