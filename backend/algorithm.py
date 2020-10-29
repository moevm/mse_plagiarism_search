from dbOperations import con, db, app, config, ALLOWED_EXTENSIONS, ALLOWED_ARCHIVES, executeQ
from pypika import Query, Table, Field, Schema, CustomFunction, Order, functions

def getAllMetaphones():
	metaphones = {}
	q = Query.from_(db.tables["CodeFragment"]).select("fileId", "metaphone").orderby('id', order=Order.asc)
	rows = executeQ(q, True)
	for row in rows:
		metaphones.setdefault(row[0], []).append(row[1])
	return metaphones
	
###############levenshtein_less_equal 

def algo(fileId):
	metaphones = getAllMetaphones()

	average = 0
	sumStud1 = 0
	sumStud2 = 0
	distances = []
	for val in metaphones[3]:
		minD = 255
		for val2 in metaphones[4]:
			q = Query.select(db.func["levenshtein"](val,val2))
			rows = executeQ(q, True)
			for row in rows:
				minD = min(minD, row[0])
		distances.append(minD)
	distances.sort()
	for i in range(len(distances)):
		if distances[i] > 25:
			print("plagiat: ", i/len(distances))
			break
	#print(len(distances), distances, distances.sort())
	
	#average = (sumStud1 + sumStud2) // 2
	
	#matches = 0

	#for item in codes[stud1].items():
		#if codes[stud2].get(item[0]):
			#matches += min(item[1], codes[stud2].get(item[0]))
			
	#print("stud", stud1, " vs stud", stud2, ":::::", matches , "/" , average, "/", matches/average*100, "%")
	#print(sumStud1, sumStud2)
	#print("stud", 1, " vs stud", 2, ":::::", sumStud1/sumStud2*100, "%")
	
#algo(3)


text1 = """
const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');
context.scale(20, 20);

const nextEl = document.getElementById('next');
const ctx = nextEl.getContext('2d');
ctx.scale(20, 20);


const pieces = 'TJLOSZI';
var rotateSound = new Audio('rotate.mp3');
var lineSound = new Audio('line.mp3');
var moveSound = new Audio('move.mp3');
var dropSound = new Audio('drop.mp3');
var themeSound = new Audio('sound.wav');

FJDKfe fj jkf sldkjf rgj

  function store(argument, value) {
            localStorage.setItem(argument, value);
        }

        function read(argument){
             return localStorage.getItem(argument);
            
        }

function arenaSweep() {
    let rowCount = 1;
    outer: for (let y = arena.length -1; y > 0; --y) {
        for (let x = 0; x < arena[y].length; ++x) {
            if (arena[y][x] === 0) {
                continue outer;
            }
        }


        const row = arena.splice(y, 1)[0].fill(0);
        arena.unshift(row);
        ++y;

        lineSound.play();

        player.score += rowCount * 10;
        rowCount *= 2;
        dropInterval-=30;
    }
}

function collide(arena, player) {
    const m = player.matrix;
    const o = player.pos;
    for (let y = 0; y < m.length; ++y) {
        for (let x = 0; x < m[y].length; ++x) {
            if (m[y][x] !== 0 &&
                (arena[y + o.y] &&
                    arena[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;
}

function createMatrix(w, h) {
    const matrix = [];
    while (h--) {
        matrix.push(new Array(w).fill(0));
    }
    return matrix;
}

function createPiece(type)
{

    if (type === 'I') {
        return [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
        ];
    } else if (type === 'L') {
        return [
            [0, 2, 0],
            [0, 2, 0],
            [0, 2, 2],
        ];
    } else if (type === 'J') {
        return [
            [0, 3, 0],
            [0, 3, 0],
            [3, 3, 0],
        ];
    } else if (type === 'O') {
        return [
            [4, 4],
            [4, 4],
        ];
    } else if (type === 'Z') {
        return [
            [5, 5, 0],
            [0, 5, 5],
            [0, 0, 0],
        ];
    } else if (type === 'S') {
        return [
            [0, 6, 6],
            [6, 6, 0],
            [0, 0, 0],
        ];
    } else if (type === 'T') {
        return [
            [0, 7, 0],
            [7, 7, 7],
            [0, 0, 0],
        ];
    }
}

function drawMatrix(matrix, offset) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                context.fillStyle = colors[value];
                context.fillRect(x + offset.x,
                    y + offset.y,
                    1, 1);
            }
        });
    });
}


function draw() {
    context.fillStyle = '#000';
    context.fillRect(0, 0, canvas.width, canvas.height);

    drawMatrix(arena, {x: 0, y: 0});
    drawMatrix(player.matrix, player.pos);
}



function drawNextEl(matrix){

    ctx.fillStyle = '#000';
    ctx.fillRect(0,0, nextEl.width, nextEl.height);


    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                ctx.fillStyle = colors[value];
                ctx.fillRect(x+1.5,
                    y+1.5 ,
                    1, 1);
            }
        });
    });
}

function merge(arena, player) {
    player.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                arena[y + player.pos.y][x + player.pos.x] = value;
            }
        });
    });

dropSound.play();
}

function rotate(matrix, dir) {
    for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
            [
                matrix[x][y],
                matrix[y][x],
            ] = [
                matrix[y][x],
                matrix[x][y],
            ];
        }
    }

    if (dir > 0) {
        matrix.forEach(row => row.reverse());
    } else {
        matrix.reverse();
    }

    rotateSound.play();
}

function playerDrop() {

    if(player.playing){
        player.pos.y++;
        if (collide(arena, player)) {
            player.pos.y--;
            merge(arena, player);
            playerReset();
            arenaSweep();
            updateScore();
        }
        dropCounter = 0;
        moveSound.play();
    }

}

function playerMove(offset) {
    if(player.playing){
        player.pos.x += offset;
        moveSound.play();
        if (collide(arena, player)) {
            player.pos.x -= offset;
        }
    }

}

function playerReset() {

    player.matrix = player.nextEl;
    player.nextEl = createPiece(pieces[pieces.length * Math.random() | 0]);
    drawNextEl(player.nextEl);
    player.pos.y = 0;
    player.pos.x = (arena[0].length / 2 | 0) -
        (player.matrix[0].length / 2 | 0);
    if (collide(arena, player)) {

       var prevScore = read(name);
       if(prevScore<player.score){
            store(player.name, player.score);
       }
        dropInterval = 1000;
        player.playing = false;
        arena.forEach(row => row.fill(0));
        player.score = 0;
        updateScore();
    }
}

function playerRotate(dir) {
    if(player.playing){
        const pos = player.pos.x;
        let offset = 1;
        rotate(player.matrix, dir);
        while (collide(arena, player)) {
            player.pos.x += offset;
            offset = -(offset + (offset > 0 ? 1 : -1));
            if (offset > player.matrix[0].length) {
                rotate(player.matrix, -dir);
                player.pos.x = pos;
                return;
            }
        }
    }


}

let dropCounter = 0;
let dropInterval = 1000;

let lastTime = 0;
function update(time = 0) {
    const deltaTime = time - lastTime;

    dropCounter += deltaTime;
    if (dropCounter > dropInterval) {
        playerDrop();
    }

    lastTime = time;

    draw();
    requestAnimationFrame(update);
}

function updateScore() {
    document.getElementById('score').innerText = player.name + ": "+ player.score ;
}

document.addEventListener('keydown', event => {


        switch (event.keyCode) {
            case 37 : playerMove(-1); break;
            case 39 : playerMove(1); break;
            case 40 : playerDrop(); break;
            case 81 : playerRotate(-1); break;
            case 87 : playerRotate(1); break;
            case 27 : {player.playing = !player.playing; }break;

        }
});

const colors = [
    null,
    '#FF0D72',
    '#0DC2FF',
    '#0DFF72',
    '#F538FF',
    '#FF8E0D',
    '#FFE138',
    '#3877FF',
];

const arena = createMatrix(12, 20);

const player = {
    name : read("nickname"),
    playing : true,
    pos: {x: 0, y: 0},
    matrix: null,
    nextEl: createPiece(pieces[pieces.length * Math.random() | 0]),
    score: 0,
};

playerReset();
updateScore();
update();

"""

text2 = """
const canvas = document.getElementById('tetris');
const context = canvas.getContext('2d');
context.scale(20, 20);

const nextEl = document.getElementById('next');
const ctx = nextEl.getContext('2d');
ctx.scale(20, 20);


const pieces = 'TJLOSZI';


  function store(argument, value) {
            localStorage.setItem(argument, value);
        }

        function read(argument){
             return localStorage.getItem(argument);
            
        }

function cleanArena() {
    let rowCount = 1;
    outer: for (let y = arena.length -1; y > 0; --y) {
        for (let x = 0; x <= arena[y].length-1; x++) {
            if (arena[y][x] === 0) {
                continue outer;
            }
        }

        const row = arena.splice(y, 1)[0].fill(0);
        arena.unshift(row);
        ++y;

        player.score += rowCount * 10;
        rowCount *= 2;
        dropInterval-=30;
    }
}

function collide(arena, player) {
    const m = player.mtx;
    var o = player.pos;
    for (let y = 0; y < m.length; ++y) {
        for (let x = 0; x < m[y].length; ++x) {
            if (m[y][x] !== 0 &&
                (arena[y + o.y] &&
                    arena[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;


}

function createMatrix(w, h) {
    const matrix = [];
    while (h--) {
        matrix.push(new Array(w).fill(0));
    }
    return matrix;
}

function createPiece(type)
{

    if (type === 'I') {
        return [
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
        ];
    } else if (type === 'L') {
        return [
            [0, 2, 0],
            [0, 2, 0],
            [0, 2, 2],
        ];
    } else if (type === 'J') {
        return [
            [0, 3, 0],
            [0, 3, 0],
            [3, 3, 0],
        ];
    } else if (type === 'O') {
        return [
            [4, 4],
            [4, 4],
        ];
    } else if (type === 'Z') {
        return [
            [5, 5, 0],
            [0, 5, 5],
            [0, 0, 0],
        ];
    } else if (type === 'S') {
        return [
            [0, 6, 6],
            [6, 6, 0],
            [0, 0, 0],
        ];
    } else if (type === 'T') {
        return [
            [0, 7, 0],
            [7, 7, 7],
            [0, 0, 0],
        ];
    }
}

function drawMatrix(matrix, offset) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                context.fillStyle = colors[value];
                context.fillRect(x + offset.x,
                    y + offset.y,
                    1, 1);
            }

        });
    });
}


function draw() {
    context.fillStyle = '#e3f3ea';  //здесь
    context.fillRect(0, 0, canvas.width, canvas.height);

    context.lineWidth = 0.01;
    context.outlineColor = "#000";
    for (let i = 0; i < 20; ++i) {
        context.beginPath();
        context.moveTo(0, (i * 20)/20); // Начало линии
        context.lineTo(240/20, (i * 20)/20); // Конец линии
        context.stroke();
        context.closePath();
    }

    for (let i = 0; i < 12; ++i) {
        context.beginPath();
        context.moveTo((i * 20)/20, 0); // Начало линии
        context.lineTo((i * 20)/20, 400/20); // Конец линии
        context.stroke();
        context.closePath();
    }


    drawMatrix(arena, {x: 0, y: 0});
    drawMatrix(player.matrix, player.pos);
}




function drawNextElement(mtx){

    ctx.fillStyle = '#e3f3ea';
    ctx.fillRect(0,0, nextEl.width, nextEl.height);


    mtx.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                ctx.fillStyle = colors[value];
                ctx.fillRect(x+1.5,
                    y+1.5 ,
                    1, 1);
            }
        });
    });
}

function merge(arena, player) {
    player.mtx.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                arena[y + player.pos.y][x + player.pos.x] = value;
            }
        });
    });
}

function rotate(matrix, dir) {
    for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
            [
                matrix[x][y],
                matrix[y][x],
            ] = [
                matrix[y][x],
                matrix[x][y],
            ];
        }
    }

    if (dir > 0) {
        matrix.forEach(row => row.reverse());
    } else {
        matrix.reverse();
    }
}

function playerDrop() {

    if(player.playing){
        player.pos.y++;
        if (collide(arena, player)) {
            player.pos.y--;
            merge(arena, player);
            playerReset();
            arenaSweep();
            updateScore();
        }
        dropCounter = 0;
    }

}

function playerMove(offset) {
    if(player.playing){
        player.pos.x += offset;
        if (collide(arena, player)) {
            player.pos.x -= offset;
        }
    }

}

function playerReset() {

    player.mtx = player.nextEl;
    player.nextEl = createPiece(pieces[pieces.length * Math.random() | 0]);
    drawNextEl(player.nextEl);
    player.pos.y = 0;
    player.pos.x = (arena[0].length / 2 | 0) -
        (player.mtx[0].length / 2 | 0);
    if (collide(arena, player)) {

       var prevScore = read(name);
       if(prevScore<player.score){
            store(player.name, player.score);
       }
        dropInterval = 1000;
        player.playing = false;
        arena.forEach(row => row.fill(0));
        player.score = 0;
        updateScore();
    }
}

function playerRotate(dir) {
    if(player.playing){
        const pos = player.pos.x;
        let offset = 1;
        rotate(player.matrix, dir);
        while (collide(arena, player)) {
            player.pos.x += offset;
            offset = -(offset + (offset > 0 ? 1 : -1));
            if (offset > player.matrix[0].length) {
                rotate(player.matrix, -dir);
                player.pos.x = pos;
                return;
            }
        }
    }


}

let dropCounter = 0;
let dropInterval = 1000;

let lastTime = 0;
function update(time = 0) {
    const deltaTime = time - lastTime;

    dropCounter += deltaTime;
    if (dropCounter > dropInterval) {
        playerDrop();
    }

    lastTime = time;

    draw();
    requestAnimationFrame(update);
}

function updateScore() {
    document.getElementById('score').innerText = player.name + ": "+ player.score ;
}

document.addEventListener('keydown', event => {


        switch (event.keyCode) {
            case 37 : playerMove(-1); break;
            case 39 : playerMove(1); break;
            case 40 : playerDrop(); break;
            case 81 : playerRotate(-1); break;
            case 38 :
            case 87 : playerRotate(1); break;
            case 27 : {player.playing = !player.playing; }break;

        }
});

const colors = [
    null,
    '#4B0082',
    '#00FA9A',
    '#8A2BE2',
    '#C71585',
    '#CD5C5C',
    '#0000FF',
    '#FF00FF',
];

const arena = createMatrix(12, 20);

const player = {
    name : read("nickname"),
    playing : true,
    pos: {x: 0, y: 0},
    matrix: null,
    nextEl: createPiece(pieces[pieces.length * Math.random() | 0]),
    score: 0,
};


// вызов
playerReset();
updateScore();
update();
"""


def algo2():
	strings1 = text1.replace("\t", "").split("\n")
	strings2 = text2.replace("\t", "").split("\n")

	metaphones1 = []
	metaphones2 = []
	
	for val in strings1:
		if len(val) > 0 and len(val)<=255:
			q = Query.select(db.func["metaphone"](val,255))
			rows = executeQ(q, True)
			for row in rows:
				if len(row[0])!=0:
					metaphones1.append(row[0])
	for val in strings2:
		if len(val) > 0 and len(val)<=255:
			q = Query.select(db.func["metaphone"](val,255))
			rows = executeQ(q, True)
			for row in rows:
				if len(row[0])!=0:
					metaphones2.append(row[0])
	#print(metaphones1)		
	#print(metaphones2)		
	distances = []
	for val in metaphones1:
		minD = 255
		for val2 in metaphones2:
			q = Query.select(db.func["levenshtein"](val,val2))
			rows = executeQ(q, True)
			for row in rows:
				#if (row[0] == 0):
					#print(val, val2)
				minD = min(minD, row[0])
		distances.append(minD)
	distances.sort()
	print(distances)
	for i in range(len(distances)):
		if distances[i] > 25:
			print("plagiat: ", i/len(distances))
			break
			
			
algo2()