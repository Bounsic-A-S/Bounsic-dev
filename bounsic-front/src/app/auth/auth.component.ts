import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import {
  ChangeDetectionStrategy,
  Component,
  Input,
  Output,
  EventEmitter,
} from '@angular/core';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AuthComponent {
  isRegisterForm = false;
  registerForm: FormGroup;
  @Input() isOpen: boolean = false; // Para controlar la visibilidad
  @Output() closeModal: EventEmitter<void> = new EventEmitter(); // Emitir evento para cerrar el modal

  constructor(private fb: FormBuilder) {
    this.registerForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  toggleForms(): void {
    this.isRegisterForm = !this.isRegisterForm;
  }

  onLogin(): void {
    console.log('Login button clicked');
    // Implement your login logic here
  }

  onRegister(): void {
    if (this.registerForm.valid) {
      console.log('Register form submitted', this.registerForm.value);
      // Implement your registration logic here
    } else {
      // Mark all fields as touched to trigger validation messages
      Object.keys(this.registerForm.controls).forEach(key => {
        const control = this.registerForm.get(key);
        control?.markAsTouched();
      });
    }
  }

  close() {
    this.closeModal.emit();
  }

}