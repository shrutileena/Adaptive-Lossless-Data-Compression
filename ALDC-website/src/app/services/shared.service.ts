import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SharedService {
  len = 0;
  len_c = 0
  constructor() { }

  getLen() {
    return this.len;
  }

  getCompressedLen() {
    return this.len_c;
  }
}
