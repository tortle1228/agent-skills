import { query } from '../db/client';
export const listItems = () => query('select * from items');
