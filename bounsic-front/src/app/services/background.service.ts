import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class BackgroundService {
  private backgroundSubject = new BehaviorSubject<string>('bg-bounsic-gradient');
  background$ = this.backgroundSubject.asObservable();

  constructor() {
    const savedBg = localStorage.getItem('background');
    if (savedBg) this.backgroundSubject.next(savedBg);
  }

  setBackground(bgClass: string) {
    localStorage.setItem('background', bgClass);
    this.backgroundSubject.next(bgClass);
  }

  get currentBackground(): string {
    return this.backgroundSubject.value;
  }
}
