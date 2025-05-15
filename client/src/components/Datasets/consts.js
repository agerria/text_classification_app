export const classColors = [
    'green',
    'gold',
    'volcano',
    'cyan',
    'orange',
    'blue',
    'purple',
    'geekblue',
    'magenta',
    'red',
]

export const getClassColor = (id)  => {
    const i  = id % classColors.length;
    return classColors[i];
}