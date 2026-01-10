export type ClassValue = string | number | null | false | undefined | ClassDictionary | ClassArray;

interface ClassDictionary {
  [key: string]: any;
}

interface ClassArray extends Array<ClassValue> {}

function toVal(mix: ClassValue): string {
  let str = '';
  if (typeof mix === 'string' || typeof mix === 'number') {
    str += mix;
  } else if (Array.isArray(mix)) {
    for (const item of mix) {
      const val = toVal(item);
      if (val) {
        if (str) str += ' ';
        str += val;
      }
    }
  } else if (mix && typeof mix === 'object') {
    for (const key in mix as ClassDictionary) {
      if ((mix as ClassDictionary)[key]) {
        if (str) str += ' ';
        str += key;
      }
    }
  }
  return str;
}

export function cn(...inputs: ClassValue[]): string {
  let str = '';
  for (const input of inputs) {
    const val = toVal(input);
    if (val) {
      if (str) str += ' ';
      str += val;
    }
  }
  return str;
}
