NUM_TOPICS = 5



GENERATE_TABLE_TOPICS_PROMPT = """你是一个数据分析专家，并且拥有广泛的知识。
我的身份是："{persona}"
我希望你根据我的身份生成 {num_topics} 个我可能感兴趣的、或者在日常生活中可能遇到的 {figure_type} 相关话题。

以下是要求：
1. 每个话题是一个表格数据的高层次总结，例如：“2021年第一季度一家杂货店的销售数据”。
2. 话题应该多样化，以帮助我生成不同的表格。每个话题应该是独特的，且不与其他话题重叠。
3. 话题与表格类型相关。请确保你提供的话题最适合在 "{figure_type}" 中进行可视化。
4. 所有话题必须用中文，即使我的身份是非中文的。
5. 列出 {num_topics} 个话题，按“|”字符分隔，例如：topic1 | topic2 | ...... | topic{num_topics}。
请不要在回答的开头或结尾添加任何额外的文本。"""



GENERATE_TABLE_DATA_PROMPT = """你是数据分析方面的专家，拥有广泛的知识，涵盖了各种主题。
我的角色是: "{persona}"
我需要一些关于"{topic}"的数据，用于生成一个{figure_type}。
以下是要求：
1. 数据结构必须适合{figure_type}。
2. 内容与主题相关，并根据我的角色进行定制。
3. 数据应当真实，内容应使用真实世界的实体名称。不要使用像xxA、xxB这样的占位符名称。
4. 数据应当多样化，包含多个数据点，以确保表格具有信息性。
5. 不要提供过多的数据，仅提供满足主题和图表类型所需的必要数据点。
6. 所有数据必须使用中文，即使角色使用非中文。
请以CSV格式提供数据，不要在开头或结尾添加额外的文本。"""



GENERATE_TABLE_DATA_JSON_PROMPT = """你是数据分析方面的专家，拥有广泛的知识涵盖各种话题。
我的身份是："{persona}"
我需要一些关于"{topic}"的数据，用于生成一个{figure_type}。
以下是要求：
1. 数据结构必须适合{figure_type}。
2. 内容与话题相关，并根据我的身份进行定制。
3. 数据应当真实，内容应使用现实世界中的实体名称，不要使用占位符名称如xxA、xxB等。
4. 数据应当多样化，包含多个数据点，以确保表格具有信息量。
5. 不要提供过多数据，只提供满足话题和图表类型的必要数据点。
6. 所有数据必须使用中文，即使我的身份是非中文的。
请以JSON格式提供数据，不要在开头或结尾添加额外的文字。"""




GENERATE_TABLE_QA_PROMPT = """你是数据分析方面的专家，擅长提出关于表格的问题。
我的身份是：“{persona}”
我希望你生成一些关于“{topic}”的“{figure_type}”的问答对，这是我会提问的内容。
我不会直接显示表格，而是提供生成表格的数据和代码。

<data>
{data}
</data>

<code>
{code}
</code>

请根据呈现的表格，提出一些人们可能会问的*合理问题*。要求如下：
1. **问题风格**：问题必须自然且与表格相关，能够帮助解释数据并理解洞察。
    (1) 问题的难度有所不同，有些问题通过简单查阅表格就能回答，而有些问题较为复杂，需要多步推理。
    (2) 问题应该能够根据表格中的*可视信息*作答。问题中不应包括任何与代码相关的细节，因为这类信息在图表中不可见。

2. **问题类型**：所有问题都应为简答题，可以根据表格中的可视信息回答。
    (1) **检索性问题**：要求表格中具体的值或事实（保持表格中的格式不变）。一些简单的问题可以直接从表格中回答，有些较难的问题可能需要结合多个行或列的数据进行筛选。
    (2) **组合性问题**：包含多个数学/逻辑运算，如求和、差值、平均值、中位数等。
    (3) **事实性问题**：要求基于数据判断特定事实是否成立（是或否）。确保有平衡的是/否问题。
    (4) **复杂推理问题**：需要对表格中的多个数据点进行多步骤推理。此类问题较为复杂，需要更深层次的数据理解。

3. **提供解释**：
    (1) 除了每个问题的*简洁答案*（尽可能简短），还要提供*逐步解释*，详细说明推理步骤。
    (2) 对于复杂推理问题，解释应更为详细，包含所有必要的步骤。

4. **回答格式**：使用“|”分隔问题、解释和简洁答案。
    (1) 格式应如下：问题 | 解释 | 简洁答案，例如，A组的平均值是多少？ | A组有5个数据点，求和结果为(34 + 45 + 23 + 56 + 12) = 170，所以平均值为170/5 = 34 | 34
    (2) 使用双换行符(\n\n)分隔问题-答案对。问题1 | 解释1 | 答案1\n\n问题2 | 解释2 | 答案2\n\n...
    (3) 不要提供过多的问题，5到10个问题足够。重点关注问题的多样性和质量，对于挑战性问题要提供非常详细的解释。
    (4) 简洁答案应尽可能简短，并直接回答问题。所有回答中的文字应使用自然语言，不使用编程术语，去除不必要的字符。

请严格遵循格式，不要在回答的开头或结尾添加额外的文字。"""



GENERATE_TABLE_CODE_LATEX_PROMPT = """你是一个数据分析专家，并擅长编写LaTeX代码来生成表格。
我的身份是："{persona}"
我有一些关于{topic}的数据，可以用来生成一个{figure_type}。

以下是数据（JSON格式）：
<data>
{data}
</data>

请编写一个LaTeX脚本，使用提供的数据生成一个{figure_type}。以下是要求：
1. **样式要求**：
    (1) 尝试富有创意地更改默认参数（例如字体、颜色、边框、阴影等），使表格样式独特。
    (2) 选择合适的设计、布局和边距，确保表格在保存时所有元素清晰可见、易于理解，并且没有文字重叠等问题。
    (3) 不要在白色背景上使用白色文本或其他浅色文本，例如当行颜色为白色时，使用深色文本。
    (3) 图中使用中文，使用 ctex 宏包。

2. **代码要求**：
    (1) 需要将提供的数据硬编码到LaTeX脚本中以生成表格。请注意LaTeX脚本的语法和格式。
    (2) 使用`standalone` LaTeX文档类来生成表格，并添加一些边框边距（`[border=xxpt]`）。**不要添加页码。**

3. **输出要求**：
    在脚本开始时添加```latex，在脚本结尾添加```，以将代码与文本分开。这将帮助我轻松提取代码。

请不要在脚本中加入任何额外的文字。你整个回应应该是LaTeX代码，可以直接执行。"""




GENERATE_TABLE_CODE_MATPLOTLIB_PROMPT = """你是数据分析专家，擅长编写代码（Python `pandas`）生成表格。
我的角色是：“{persona}”
我有一些关于{topic}的数据，可以用来生成一个{figure_type}。

以下是数据（CSV格式，已加载为pd.DataFrame）：
<data>
{data}
</data>

请定义一个Python函数（使用`pandas`）叫做`generate_table`，利用提供的数据生成一个{figure_type}。以下是要求：
1. **样式要求**：
    (1) 尝试创意化并修改默认参数（例如字体、颜色、边框、阴影等），使表格样式独特。通过使用`plt.style.use('{style_name}')`来设置样式。
    (2) 选择适当的设计尺度（例如列宽），确保每个单元格中的信息清晰易懂，没有文本重叠等。
    (3) 图中使用中文。

2. **代码要求**：创建一个名为`generate_table`的函数，使用`pandas`生成表格。
    (1) 提供的已加载为pd.DataFrame的数据作为该函数的第一个参数。该函数没有其他参数。你可能需要根据要求和设计调整数据格式。
    (2) 记得在脚本开始时导入必要的库（例如`import numpy as np`，`import pandas as pd`，`import matplotlib.pyplot as plt`等）。
    (3) `generate_table`函数应该将表格保存到BytesIO中，然后返回表格作为PIL图像对象。**不要关闭BytesIO对象**。
    (4) 选择适当的边距、分辨率，并确保使用紧凑布局，确保表格保存时所有元素都可见。
    (5) 只定义该函数，不要调用它。不显示表格。无需显示示例用法。

3. **输出要求**：
    在脚本开始处添加```python，在结尾处添加```，将代码与文本分开。这将帮助我轻松提取代码。

请不要在脚本中回答任何附加文本。你的整个响应应该是可以直接执行的Python代码。"""




GENERATE_TABLE_CODE_PLOTLY_PROMPT = """你是数据分析专家，擅长编写代码（Python `plotly`）来生成表格。
我的身份是："{persona}"
我有一些关于{topic}的数据，可以用来生成一个{figure_type}。

这是数据（CSV格式，已经加载为pd.DataFrame）：
<data>
{data}
</data>

请定义一个名为`generate_table`的Python函数（使用`plotly`）来生成一个{figure_type}，使用提供的数据。以下是要求：
1. **样式要求**：
    (1) 尽量具有创意，修改默认参数（例如，字体、颜色、边框、阴影等），使表格样式独特。
    (2) 选择合适的设计比例（例如，列宽），确保每个单元格中的信息清晰易懂，没有文本重叠等问题。
    (3) 图中使用中文。

2. **代码要求**：创建一个名为`generate_table`的函数，使用`plotly`生成表格。不要使用matplotlib或其他库。
    (1) 数据作为第一个参数传递给函数，已作为pd.DataFrame加载。函数没有其他参数。你可能需要调整数据格式以符合`plotly`的规范。
    (2) 记得在脚本开始时导入必要的库（例如，`import numpy as np`，`import plotly.express as px`）。
    (3) `generate_table`函数应将表格保存为BytesIO对象，并返回该表格作为PIL Image对象。**不要关闭BytesIO对象**。
    (4) 选择合适的边距和紧凑布局，确保保存的表格所有元素都可见。
    (5) 只定义函数，不要调用它。不要显示表格。保存表格时确保分辨率足够清晰。无需显示示例用法。

3. **输出要求**：
    在脚本的开始处放置```python，在结束处放置```，以便将代码与文本分开。这样可以帮助我轻松提取代码。

请不要在脚本中添加任何额外的文本。你的整个回答应为可以直接执行的Python代码。"""






GENERATE_TABLE_CODE_HTML_PROMPT = """你是一位专家级的网页设计师，擅长编写HTML来创建表格。
我的角色是："{persona}"
我有一些关于{topic}的数据，可以用来生成一个{figure_type}。

以下是材料（JSON格式）：
<data>
{data}
</data>

请使用HTML和CSS来根据提供的数据生成一个{figure_type}。以下是要求：
1. **样式要求**：可以自由使用任何CSS框架、库、JavaScript插件或其他工具来创建表格。
    (1) 尝试富有创意，并使用CSS使网页的样式、字体、颜色、边框和视觉布局独特。设计表格时要考虑角色、主题和表格类型。
    (2) 选择合适的设计比例（例如列宽、单元格大小、边距等），确保表格中的信息清晰易懂，不会出现文字重叠等问题。
    (3) 图中使用中文。

2. **代码要求**：
    (1) 需要将提供的数据硬编码到HTML脚本中以生成文档。注意HTML脚本的语法和格式。
    (2) 所有内容都放在一个HTML文件中。不要使用外部的CSS或JavaScript文件。

3. **输出要求**：
    在脚本的开头放置```html，结尾放置```以将代码与文本分开。

请不要在脚本中添加任何额外的文字，整个回答应为可以直接执行的HTML代码。"""
