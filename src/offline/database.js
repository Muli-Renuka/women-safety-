import Dexie from 'dexie';
export const db=new Dexie('shadowmode-local'); db.version(1).stores({events:'event_uuid,created_at,status',contacts:'++id,name',meta:'key'});
export async function saveEvent(event){await db.events.put(event);return event;}
export async function getEvents(){return db.events.orderBy('created_at').reverse().toArray();}
export async function clearLocalEvents(){await db.events.clear();}
