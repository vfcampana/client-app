import { Block } from "./Blocks";

export interface Lote {
    id?: number;
    id_usuario?: number;
    nome: string;
    preco: number;
    observacoes: string;
    status: number;
    blocos?: (Block | number)[];
}