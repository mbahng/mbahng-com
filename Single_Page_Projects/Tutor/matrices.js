function coef(num, addsign=true) {
    if (num == 0 || num == 1) { return "+";} 
    else if (num == -1) {return "-";} 
    else if (num > 0 && addsign==true) {return `+ ${num}`;}
    else {return num;}
}

function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length !== b.length) return false;

    for (var i = 0; i < a.length; ++i) {
      if (a[i] !== b[i]) return false;
    }
    return true;
  }

function VecRandGen(level) {
    if (level == 1) {
        return Math.round((Math.random() * 10) - 5);
    } else if (level == 2) {
        return Math.round((Math.random() * 20) - 10);
    } else if (level == 3) {
        return Math.round((Math.random() * 40) - 20);
    }
}

class matrix {
    constructor(n, m, level) {
        this.n = n; 
        this.m = m; 
        this.level = level; 
        var array_matrix = []; 
        for (let i = 0; i < this.n; i++) {
            array_matrix.push([])
            for (let j = 0; j < this.m; j++) {
                let element = VecRandGen(level);
                array_matrix[i].push(element); 
            }
        }
        this.array = array_matrix;
    }

    latexify() {
        var latex_matrix = "\\begin{pmatrix} "; 
        for (let i =  0; i < this.n; i++) {
            let row = ""; 
            for (let j = 0; j < this.m; j++) {
                row += `${this.array[i][j]} & `; 
            }
            row = row.slice(0, -2) + "\\\\ "; 
            latex_matrix += row; 
        }
        latex_matrix = latex_matrix.slice(0, -4) + " \\end{pmatrix}"; 
        return latex_matrix; 
    }
}

function scalarMult(scalar, matrix_obj) {
    var new_matrix_array = []; 
    for (let i = 0; i < matrix_obj.n; i++) {
        new_matrix_array.push([]); 
        for (let j = 0; j < matrix_obj.m; j++) {
            new_matrix_array[i].push(matrix_obj.array[i][j] * scalar); 
        }
    }
    let newMatrixObject = new matrix(matrix_obj.n, matrix_obj.m, matrix_obj.level); 
    newMatrixObject.array = new_matrix_array; 
    return newMatrixObject; 
}

function addMatrix(matrix_obj1, matrix_obj2) {
    if ((matrix_obj1.n != matrix_obj2.n) || (matrix_obj1.m != matrix_obj2.m)) {
        return undefined; 
    }
    const N = matrix_obj1.n; 
    const M = matrix_obj1.m; 
    var new_matrix_array = []; 
    for (let i = 0; i < N; i++) {
        new_matrix_array.push([]); 
        for (let j = 0; j < M; j++) {
            new_matrix_array[i].push(matrix_obj1.array[i][j] + matrix_obj2.array[i][j]); 
        }
    }
    var newMatrixObject = new matrix(N, M, matrix_obj1.level); 
    newMatrixObject.array = new_matrix_array; 
    return newMatrixObject; 
}

function multMatrix(matrix_obj1, matrix_obj2) {
    if (matrix_obj1.m != matrix_obj2.n) {
        return undefined; 
    }
    var new_matrix_array = []; 
    const N = matrix_obj1.n; 
    const M = matrix_obj1.m; 
    const P = matrix_obj2.m; 
    for (let i = 0; i < N; i++) {
        new_matrix_array.push([]); 
        for (let j = 0; j < P; j++) {
            let new_element = 0; 
            for (let k = 0; k < M; k++) {
                new_element += matrix_obj1.array[i][k] * matrix_obj2.array[k][j]; 
            }
            new_matrix_array[i].push(new_element); 
        }
    }
    let newMatrixObject = new matrix(N, P, matrix_obj1.level); 
    newMatrixObject.array = new_matrix_array; 
    return newMatrixObject;
}

function transpose(matrix_obj) {
    N = matrix_obj.m; 
    M = matrix_obj.n; 
    transposed_matrix = new matrix(N, M, 1); 
    array = []; 
    for (let i = 0; i < N; i++) {
        let row = []; 
        for (let j = 0; j < M; j++) {
            row.push(matrix_obj.array[j][i]);
        }
        array.push(row);
    }
    transposed_matrix.array = array; 
    return transposed_matrix; 
}

function generateLinCombMatrix(level) {
    const N = Math.round((Math.random() * 3) + 1); 
    const M = Math.round((Math.random() * 3) + 1); 
    const no_of_terms = Math.round((Math.random() * 4) + 1); 
    var scalar_array = []; 
    var matrix_array = []; 
    for (let i = 0; i < no_of_terms; i++) {
        scalar_array.push(Math.round((Math.random() * 12) - 6)); 
        var obj = new matrix(N, M, level); 
        matrix_array.push(obj); 
    }
    for (let i = 0; i < scalar_array.length; i++) {
        if (scalar_array[i] == 0) {
            scalar_array[i] = 1;
        }
    }
    var exercise = ""; 
    var solution = scalarMult(0, new matrix(N, M, 1)); 
    
    for (let i = 0; i < no_of_terms; i++) {
        exercise += `${coef(scalar_array[i])} ${matrix_array[i].latexify()} `; 
        solution = addMatrix(solution, scalarMult(scalar_array[i], matrix_array[i]));
    }
    if (exercise.charAt(0) == '+') {exercise = exercise.substring(1);}
    const solution_latex = solution.latexify();
    return [`Compute the following linear combination: \\[${exercise} \\]`, solution, solution_latex]; 
}

function generateMatrixMult(level) {
    const N = Math.round((Math.random() * 3) + 1); 
    const M = Math.round((Math.random() * 3) + 1); 
    const P = Math.round((Math.random() * 3) + 1); 
    const matrix1 = new matrix(N, M, level); 
    const matrix2 = new matrix(M, P, level); 
    const exercise = `${matrix1.latexify()} \\, ${matrix2.latexify()}`; 
    const solution = multMatrix(matrix1, matrix2); 
    const solution_latex = solution.latexify(); 
    return [`Multiply the following matrices: \\[${exercise} \\]`, solution, solution_latex]; 
}

function generateDotProduct(level) {
    const dim = Math.round((Math.random() * 4) + 1); 
    const vector1 = new matrix(dim, 1, level); 
    const vector2 = new matrix(dim, 1, level); 
    const vector1T = transpose(vector1); 
    const exercise = `${vector1.latexify()} \\cdot ${vector2.latexify()}`
    const solution = multMatrix(vector1T, vector2); 
    const solution_latex = solution.array[0][0]
    return [`Compute the following dot product: \\[ ${exercise} \\]`, solution, solution_latex]; 
}

function generateOuterProduct(level) {
    const dim1 = Math.round((Math.random() * 3) + 1); 
    const dim2 = Math.round((Math.random() * 3) + 1); 
    const vector1 = new matrix(dim1, 1, level); 
    const vector2 = new matrix(dim2, 1, level); 
    const vector2T = transpose(vector2); 
    const exercise = `${vector1.latexify()} \\odot ${vector2.latexify()}`
    const solution = multMatrix(vector1, vector2T); 
    const solution_latex = solution.latexify(); 
    return [`Compute the following outer product: \\[ ${exercise} \\]`, solution, solution_latex]; 
}

function generateCrossProduct(level) {
    const vector1 = new matrix(3, 1, level); 
    const vector2 = new matrix(3, 1, level); 
    const exercise = `${vector1.latexify()} \\times ${vector2.latexify()}`
    const a1 = vector1.array[0][0]; 
    const a2 = vector1.array[1][0]; 
    const a3 = vector1.array[2][0]; 
    const b1 = vector2.array[0][0]; 
    const b2 = vector2.array[1][0]; 
    const b3 = vector2.array[2][0]; 

    const solution = new matrix(3, 1, level); 
    solution.array[0][0] = a2 * b3 - a3 * b2; 
    solution.array[1][0] = a3 * b1 - a1 * b3; 
    solution.array[2][0] = a1 * b2 - a2 * b1; 
    const solution_latex = solution.latexify(); 
    return [`Compute the following cross product: \\[ ${exercise} \\]`, solution, solution_latex]; 
}

function generateTensorProduct(level) {
    const dim1 = Math.round((Math.random() * 2) + 1); 
    const dim2 = Math.round((Math.random() * 2) + 1); 
    const vector1 = new matrix(dim1, 1, level); 
    const vector2 = new matrix(dim2, 1, level); 
    const exercise = `${vector1.latexify()} \\otimes ${vector2.latexify()}`;

    const outerproduct = multMatrix(vector1, transpose(vector2)); 
    const solution = new matrix(dim1 * dim2, 1, level); 
    for (let i = 0; i < dim1; i++) {
        for (let j = 0; j < dim2; j++) {
            let element = outerproduct.array[i][j]; 
            solution.array[dim2 * i + j][0] = element; 
        }
    }
    const solution_latex = solution.latexify(); 
    
    return [`Compute the following tensor product: \\[ ${exercise} \\]`, solution, solution_latex]; 
}

function generateVectorProduct(level) {
    const type = Math.floor(Math.random() * 4); 
    if (type == 0) {
        return generateCrossProduct(level); 
    } else if (type == 1) {
        return generateOuterProduct(level); 
    } else if (type == 2) {
        return generateTensorProduct(level); 
    } else {
        return generateDotProduct(level); 
    }
}


var func_dictM = {
    "Matrix Addition & Scalar Multiplication" : generateLinCombMatrix, 
    "Matrix Multiplication" : generateMatrixMult, 
    "Vector Products" : generateVectorProduct
}

var section_noM = 0;
function GenerateMatrixExercises(no_Q) { 
    section_noM += 1;
    var levelM = document.getElementById("Dropdown_LevelM").value;
    var func_nameM = func_dictM[document.getElementById("Dropdown_ConvertM").value];
    const matrix_section = document.getElementById("Vectors_Matrices");
    var sectionM = document.createElement('div'); 
    sectionM.style = "border: solid 1px; margin-bottom: 2%;"; 
    matrix_section.appendChild(sectionM); 
    
    var section_headerM = document.createElement('div'); 
    section_headerM.style = "border-bottom: solid 1px black; display: flex; height: 30px;"; 
    sectionM.appendChild(section_headerM); 

    var titleM = document.createElement('h3'); 
    titleM.innerHTML = `${document.getElementById("Dropdown_ConvertM").value} [Lvl.${levelM}]`;
    titleM.style = "border: solid 0px green; width: 57%; margin: 4px 10px;" 

    var title_solutionsM = document.createElement('h3');
    title_solutionsM.innerHTML = `Solutions`; 
    title_solutionsM.style = "margin: 4px 25px;"; 

    var solution_buttonM = document.createElement('button'); 
    solution_buttonM.innerHTML = `Section ${section_noM} Solutions`; 
    solution_buttonM.classList.add("Solution_ButtonM"); 
    solution_buttonM.style = "width: 20%; height: 24px; margin: 3px 0px; display: none; position: absolute; right: 20px; "; 
    
    section_headerM.appendChild(titleM); 
    section_headerM.appendChild(title_solutionsM); 
    section_headerM.appendChild(solution_buttonM);

    solution_buttonM.onclick = function() {
        var numberM = solution_buttonM.innerHTML[8];
        var solutionsM = document.getElementsByClassName(`section${numberM}solutions`);
        for (let i = 0; i < solutionsM.length; i++) {
            solutionsM[i].style = "position: absolute; left: 80%; display: inline-block;"; 
        }
    };
    listM = document.createElement('ol'); 
    listM.style = "margin-left: 0px; padding: 0px 20px; "

    for (let i = 0; i <= no_Q ; i++) {
        line = document.createElement('li');
        line.style = "margin: 3px 0px; border: solid 1px black; width: 99%; padding:1px; height: 150px; position: relative; margin-right: 0px"; 
        let ex_sol = func_nameM(levelM);
        
        var exercise = document.createElement('span'); 
        exercise.style = "float: left; width: 55%;"; 
        exercise.innerHTML = `${ex_sol[0]}`;
        line.appendChild(exercise); 
        
        var input_log = document.createElement('textarea'); 
        input_log.setAttribute('cols', 25);
        input_log.setAttribute('rows', 7);
        input_log.style = "margin-top: 5px; position: absolute; left: 60%;";
        
        input_log.setAttribute("id", `Input${section_noM}.${i}M`);
        line.appendChild(input_log); 

        MathJax.Hub.Queue(["Typeset", MathJax.Hub, line]);

        if (i == 0) {continue;}
        listM.appendChild(line);

        var reply_click = function() {
            const numberM = this.id.slice(6, -1); 
            var input_information_draft = document.getElementById(`Input${numberM}M`).value.split("\n"); 
            var input_information = []; 
            for (let i=0; i < input_information_draft.length; i++) {
                let row = input_information_draft[i].replace(/ /g,'').split(","); 
                for (let j=0; j < row.length; j++) {
                    row[j] = parseInt(row[j]);
                }
                input_information.push(row); 
            }
            document.getElementById(`Input${numberM}M`).disabled = true;
            var SameMatrix = true; 
            if (input_information.length != ex_sol[1].array.length) {
                SameMatrix = false; 
            }
            for (let row=0; row < input_information.length; row++) {
                if (arraysEqual(input_information[row], ex_sol[1].array[row])==false) {
                    SameMatrix = false; 
                }
            }
            if (SameMatrix) {
                document.getElementById(`Solution${numberM}M`).style = "position: absolute; left: 80%; display: auto; color: rgb(11, 225, 0);"; 
            } 
            else {
                document.getElementById(`Solution${numberM}M`).style = "position: absolute; left: 80%; display: auto; color: red;"; 
            }

        }

        var submit_button = document.createElement('button'); 
        submit_button.innerHTML = `Submit`; 
        submit_button.setAttribute("id",`Button${section_noM}.${i}M`);
        submit_button.onclick = reply_click; 
        submit_button.style = "width: 120px; height: 20px;padding: 1px 1px; display: auto; position: absolute; left: 60%; bottom: 5px;"; 
        line.appendChild(submit_button); 

        var solutionM = document.createElement('span'); 
        solutionM.style = "position: absolute; left: 55%; display: none; color: blue;"; 
        solutionM.setAttribute("class", `section${section_noM}solutionsM`);
        solutionM.setAttribute("id", `Solution${section_noM}.${i}M`)
        line.appendChild(solutionM); 
        solutionM.innerHTML = `${ex_sol[2]}`; 
        solutionM.value = `${ex_sol[2]}`.slice(1, -1);
        
    }
    sectionM.appendChild(listM); 
} 