import copy
import io
import json
import os

from pipeline.utils.anthropic_support import CustomAnthropic

from datadreamer import DataDreamer
from datadreamer.llms import OpenAI
from datadreamer.steps import concat

from .matplotlib_chart_pipeline import MatplotlibChartPipeline
from .vegalite_chart_pipeline import VegaLiteChartPipeline
from .plotly_chart_pipeline import PlotlyChartPipeline
from .latex_chart_pipeline import LaTeXChartPipeline
from .html_chart_pipeline import HTMLChartPipeline

from .latex_table_pipeline import LaTeXTablePipeline
from .plotly_table_pipeline import PlotlyTablePipeline
from .html_table_pipeline import HTMLTablePipeline

from .latex_document_pipeline import LaTeXDocumentPipeline
from .html_document_pipeline import HTMLDocumentPipeline

from .graphviz_diagram_pipeline import GraphvizDiagramPipeline
from .latex_diagram_pipeline import LaTeXDiagramPipeline
from .mermaid_diagram_pipeline import MermaidDiagramPipeline
from PIL import Image

# 查看dict整体结构
def print_keys_recursively(d):
    for key, value in d.items():
        print(key)
        # 如果值是字典，递归调用自身
        if isinstance(value, dict):
            print_keys_recursively(value)
            
# 存数据
def save_data_with_format(data, folder_path, output_jsonl_file):
    # 创建目标文件夹（如果不存在）
    os.makedirs(folder_path, exist_ok=True)
    
    formatted_data = []
    
    
    # 初始化新的格式化记录
    formatted_record_origin = {
        "image": "",
        "conversations": [],
        "width": 0,
        "height": 0
    }
    for idx in range(len(data["data"])):
        formatted_record = copy.deepcopy(formatted_record_origin)
        # 定义保存的图像路径
        image_path = os.path.join(folder_path, f"image_{idx}.jpg")
        
        # 将 bytes 转换为图片并保存为 JPG 格式
        try:
            image = Image.open(io.BytesIO(data["image"][idx]["bytes"]))
            image = image.convert("RGB")  # 确保保存为 RGB 格式
            image.save(image_path, format="JPEG")
            
            # 更新格式化记录
            formatted_record["image"] = image_path
            formatted_record["width"], formatted_record["height"] = image.size
            formatted_record["conversations"] = []
            for qa in eval(data['qa'][idx]):
            
                formatted_record["conversations"].append({"from": "human", "value": f"<image>\n{qa['question']}"})
                formatted_record["conversations"].append({"from": "human", "value": qa['answer']})

            formatted_record["topic"] = data["topic"][idx]
            formatted_record["explanation"] = [e["explanation"] for e in eval(data["qa"][idx])]
            formatted_record["code"] = data["code"][idx]
        except Exception as e:
            print(f"Error saving image: {e}")
            continue
        
        formatted_data.append(formatted_record)
    
    # 保存格式化数据到 JSONL 文件
    with open(output_jsonl_file, 'w', encoding='utf-8') as jsonl_file:
        for item in formatted_data:
            jsonl_file.write(json.dumps(item, ensure_ascii=False) + '\n')

def run_datadreamer_session(args):
    if args.qa:
        os.environ["GENERATE_QA"] = "true"
    else:
        os.environ["GENERATE_QA"] = "false"
 
    with DataDreamer("./session_output"):
        # Load GPT-4
        gpt_4o = OpenAI(
            model_name="gpt-4o",
            api_key=args.openai_api_key,
            system_prompt="You are a helpful data scientist.",
        )

        gpt_4o_mini = OpenAI(
            model_name="gpt-4o-mini",
            api_key=args.openai_api_key,
            system_prompt="You are a helpful data scientist.",
        )

        claude_sonnet = CustomAnthropic(
            model_name="claude-3-5-sonnet-20240620",
            api_key=args.anthropic_api_key,
        )

        client_302_claude = OpenAI(
            model_name="claude-3-5-sonnet-20241022",
            api_key=args.anthropic_api_key,
            base_url="https://api.302.ai"
        )

        client_302_gpt4o = OpenAI(
            model_name="gpt-4o",
            api_key=args.anthropic_api_key,
            base_url="https://api.302.ai"
        )

        
        if args.llm == "gpt-4o": llm = gpt_4o
        elif args.llm == "claude-sonnet": llm = claude_sonnet
        elif args.llm == "gpt-4o-mini": llm = gpt_4o_mini
        elif args.llm == "gpt-4o-302": llm = client_302_gpt4o

        if args.code_llm == "gpt-4o": code_llm = gpt_4o
        elif args.code_llm == "claude-sonnet": code_llm = claude_sonnet
        elif args.code_llm == "gpt-4o-mini": code_llm = gpt_4o_mini
        elif args.code_llm == "claude-sonnet-302": code_llm = client_302_claude

        # Choose which pipelines to run
        pipelines = {
            "Generate Matplotlib Charts": MatplotlibChartPipeline,
            "Generate Vega-Lite Charts": VegaLiteChartPipeline,
            "Generate Plotly Charts": PlotlyChartPipeline,
            "Generate LaTeX Charts": LaTeXChartPipeline,
            "Generate HTML Charts": HTMLChartPipeline,
            "Generate LaTeX Tables": LaTeXTablePipeline,
            "Generate Plotly Tables": PlotlyTablePipeline,
            "Generate HTML Tables": HTMLTablePipeline,
            "Generate LaTeX Documents": LaTeXDocumentPipeline,
            "Generate HTML Documents": HTMLDocumentPipeline,
            "Generate Graphviz Diagrams": GraphvizDiagramPipeline,
            "Generate LaTeX Diagrams": LaTeXDiagramPipeline,
            "Generate Mermaid Diagrams": MermaidDiagramPipeline,
        }
        pipelines = {
            k: v
            for k, v in pipelines.items()
            if v.__name__ in [p.strip() for p in args.pipelines.split(",")]
        }

        # Choose how many visualizes per pipeline
        if "," in args.num:
            nums = [int(n.strip()) for n in args.num.strip(",")]
            assert len(nums) == len(pipelines)
        else:
            nums = [int(args.num)] * len(pipelines)
        
        # Get figure types
        figure_types = [figure_type.strip() for figure_type in args.types.split(",")]

        # Run each selected pipeline
        synthetic_visuals = [
            pipeline(
                pipeline_name,
                args={
                    "llm": llm,
                    "code_llm": code_llm,
                    "batch_size": args.batch_size,
                    "code_batch_size": args.code_batch_size,
                    "n": num,
                    "seed": args.seed,
                    "figure_types": figure_types,
                    "qa": args.qa,
                },
                force=args.force,
            )
            for num, (pipeline_name, pipeline) in zip(nums, pipelines.items())
        ]

        # Combine results from each pipeline
        scifi_dataset = concat(
            *synthetic_visuals, name="Combine results from all pipelines"
        )

        # Preview n rows of the dataset
        print(scifi_dataset.head(n=5))

        # save to train format
        data = scifi_dataset.export_to_dict() #.publish_to_hf_hub(args.name, private=True)
        # print_keys_recursively(data)
        # print(data)
        save_path = f"results/{args.name}/images"
        save_jsonl = f"results/{args.name}/{args.name}.jsonl"
        save_data_with_format(data, save_path, save_jsonl)

        