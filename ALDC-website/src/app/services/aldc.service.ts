import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AldcService {

  baseApiURL = "http://127.0.0.1:5000/"

  constructor(private http: HttpClient) { }

  compress(file: File) {
    const formData = new FormData();
    formData.append("file",file,file.name);
    return this.http.post(this.baseApiURL + "api/compress",formData);
  }
}
