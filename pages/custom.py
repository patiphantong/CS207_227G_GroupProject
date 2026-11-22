import streamlit as st

st.subheader("🛠️ Custom Application")
st.info("Student task: build your own math/AI-related application here.")

# TODO 4: Add at least one new or extended feature.
# You may extend Statistics, Bayes, or Markov, or choose another topic
# related to Mathematics for AI (e.g., Gradient Descent or Matrix).
# Include: user input, calculation/processing, and output or visualization.
import numpy as np
import pandas as pd


def create_matrix_input(title: str, rows: int, cols: int, key: str) -> np.ndarray:
    st.markdown(f"**{title}**")

    default_data = pd.DataFrame(
        np.zeros((rows, cols), dtype=float),
        columns=[f"Col {i + 1}" for i in range(cols)],
    )

    edited_data = st.data_editor(
        default_data,
        key=key,
        num_rows="fixed",
        hide_index=True,
        use_container_width=True,
        column_config={
            column: st.column_config.NumberColumn(
                column,
                help="กรอกตัวเลขในเมทริกซ์",
                step=1.0,
            )
            for column in default_data.columns
        },
    )
    return edited_data.to_numpy(dtype=float)


def show_matrix(matrix: np.ndarray, title: str) -> None:
    """Display a matrix as a readable table."""
    st.markdown(f"**{title}**")
    result_df = pd.DataFrame(
        matrix,
        columns=[f"Col {i + 1}" for i in range(matrix.shape[1])],
        index=[f"Row {i + 1}" for i in range(matrix.shape[0])],
    )
    st.dataframe(result_df, use_container_width=True)


def show_dimensions(matrix: np.ndarray, name: str) -> None:
    """Display the dimensions of a matrix."""
    st.caption(f"{name}: {matrix.shape[0]} rows × {matrix.shape[1]} columns")


st.subheader("🧮 Matrix Calculator")
st.write(
    "เครื่องมือคำนวณเมทริกซ์ตามเนื้อหา Linear Algebra "
    "ประกอบด้วยการบวก ลบ คูณเมทริกซ์ และการแปลงเวกเตอร์"
)
st.markdown("---")

operation = st.selectbox(
    "เลือกการคำนวณ",
    [
        "Matrix Addition (+)",
        "Matrix Subtraction (−)",
        "Matrix Multiplication (×)",
        "Matrix Transformation (T × x)",
    ],
)
st.info(
    "วิธีใช้: กำหนดขนาดเมทริกซ์ จากนั้นกรอกตัวเลขลงในตาราง "
    "แล้วกดปุ่ม Calculate เพื่อดูผลลัพธ์"
)
# 1. Matrix Addition and Subtraction
if operation in ["Matrix Addition (+)", "Matrix Subtraction (−)"]:
    st.markdown("### Matrix Dimensions")
    col1, col2 = st.columns(2)

    with col1:
        rows = st.number_input(
            "Number of rows",
            min_value=1,
            max_value=6,
            value=2,
            step=1,
            key="add_sub_rows",
        )
    with col2:
        cols = st.number_input(
            "Number of columns",
            min_value=1,
            max_value=6,
            value=2,
            step=1,
            key="add_sub_cols",
        )

    rows, cols = int(rows), int(cols)
    st.caption(
        f"เมทริกซ์ A และ B ต้องมีขนาดเท่ากัน คือ {rows} × {cols}"
    )
    left, right = st.columns(2)
    with left:
        matrix_a = create_matrix_input("Matrix A", rows, cols, "add_sub_matrix_a")
    with right:
        matrix_b = create_matrix_input("Matrix B", rows, cols, "add_sub_matrix_b")

    if st.button("Calculate", type="primary", use_container_width=True):
        if operation == "Matrix Addition (+)":
            result = matrix_a + matrix_b
            symbol = "+"
        else:
            result = matrix_a - matrix_b
            symbol = "−"

        st.markdown("---")
        st.subheader("📊 Calculation Result")
        show_matrix(matrix_a, "Matrix A")
        show_matrix(matrix_b, "Matrix B")
        st.markdown(f"### A {symbol} B")
        show_matrix(result, "Result Matrix")
        st.success(
            f"คำนวณสำเร็จ: เมทริกซ์ผลลัพธ์มีขนาด "
            f"{result.shape[0]} × {result.shape[1]}"
        )

# 2. Matrix Multiplication

elif operation == "Matrix Multiplication (×)":
    st.markdown("### Matrix Dimensions")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Matrix A**")
        a_rows = st.number_input(
            "Rows of A", 1, 6, 2, 1, key="mul_a_rows"
        )
        a_cols = st.number_input(
            "Columns of A", 1, 6, 2, 1, key="mul_a_cols"
        )

    with col2:
        st.markdown("**Matrix B**")
        b_rows = st.number_input(
            "Rows of B", 1, 6, 2, 1, key="mul_b_rows"
        )
        b_cols = st.number_input(
            "Columns of B", 1, 6, 2, 1, key="mul_b_cols"
        )

    a_rows, a_cols = int(a_rows), int(a_cols)
    b_rows, b_cols = int(b_rows), int(b_cols)
    if a_cols == b_rows:
        st.success(
            f"คูณกันได้: ({a_rows} × {a_cols}) × "
            f"({b_rows} × {b_cols}) จะได้ผลลัพธ์ขนาด "
            f"{a_rows} × {b_cols}"
        )
    else:
        st.warning(
            "คูณเมทริกซ์คู่นี้ไม่ได้ เพราะจำนวน Columns ของ A "
            "ต้องเท่ากับจำนวน Rows ของ B"
        )

    left, right = st.columns(2)
    with left:
        matrix_a = create_matrix_input(
            "Matrix A", a_rows, a_cols, "mul_matrix_a"
        )
    with right:
        matrix_b = create_matrix_input(
            "Matrix B", b_rows, b_cols, "mul_matrix_b"
        )

    if st.button("Calculate", type="primary", use_container_width=True):
        if a_cols != b_rows:
            st.error(
                "ไม่สามารถคูณเมทริกซ์ได้: "
                "Columns ของ A ต้องเท่ากับ Rows ของ B"
            )
        else:
            result = matrix_a @ matrix_b

            st.markdown("---")
            st.subheader("📊 Calculation Result")
            show_matrix(matrix_a, "Matrix A")
            show_matrix(matrix_b, "Matrix B")
            st.markdown("### A × B")
            show_matrix(result, "Result Matrix")

            with st.expander("ดูตัวอย่างวิธีคำนวณ Row-by-Column"):
                row_index = 0
                col_index = 0
                terms = [
                    f"({matrix_a[row_index, k]:g} × "
                    f"{matrix_b[k, col_index]:g})"
                    for k in range(a_cols)
                ]
                calculation = " + ".join(terms)
                st.latex(
                    r"C_{1,1} = " + calculation
                    + f" = {result[row_index, col_index]:g}"
                )
                st.caption(
                    "นำแถวที่ 1 ของ Matrix A มาคูณกับหลักที่ 1 "
                    "ของ Matrix B แล้วนำผลคูณมาบวกกัน"
                )

            st.success(
                f"คำนวณสำเร็จ: ผลลัพธ์มีขนาด "
                f"{result.shape[0]} × {result.shape[1]}"
            )

# 3. Matrix Transformation
else:
    st.markdown("### Transformation Matrix")
    col1, col2 = st.columns(2)

    with col1:
        rows = st.number_input(
            "Number of output dimensions (rows)",
            min_value=1,
            max_value=6,
            value=2,
            step=1,
            key="transform_rows",
        )
    with col2:
        cols = st.number_input(
            "Number of input dimensions (columns)",
            min_value=1,
            max_value=6,
            value=2,
            step=1,
            key="transform_cols",
        )

    rows, cols = int(rows), int(cols)

    st.caption(
        f"Transformation Matrix: {rows} × {cols} | "
        f"Input Vector ต้องมี {cols} ค่า"
    )

    matrix = create_matrix_input(
        "Transformation Matrix (T)", rows, cols, "transform_matrix"
    )

    st.markdown("**Input Vector (x)**")
    vector_values = []
    vector_columns = st.columns(cols)

    for index, column in enumerate(vector_columns):
        with column:
            value = st.number_input(
                f"x{index + 1}",
                value=0.0,
                step=1.0,
                key=f"transform_vector_{index}",
            )
            vector_values.append(value)

    vector = np.array(vector_values, dtype=float).reshape(cols, 1)

    if st.button("Transform Vector", type="primary", use_container_width=True):
        result = matrix @ vector

        st.markdown("---")
        st.subheader("📊 Transformation Result")
        left, right = st.columns(2)

        with left:
            show_matrix(matrix, "Transformation Matrix (T)")
            st.markdown("**Input Vector (x)**")
            st.dataframe(
                pd.DataFrame(vector, columns=["Value"]),
                use_container_width=True,
                hide_index=True,
            )

        with right:
            st.markdown("**Output Vector (T × x)**")
            st.dataframe(
                pd.DataFrame(result, columns=["Output"]),
                use_container_width=True,
                hide_index=True,
            )

        st.success(
            f"แปลงเวกเตอร์สำเร็จ: จาก {cols} มิติ "
            f"เป็น {rows} มิติ"
        )

st.markdown("---")
st.caption(
    "CS207 Mathematics for AI | Matrix Operations and Feature Transformation"
)
