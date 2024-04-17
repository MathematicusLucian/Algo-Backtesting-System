import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { provideServerRendering } from '@angular/platform-server';
// import { BrowserModule } from '@angular/platform-browser';
// import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
// import { FormsModule } from '@angular/forms';
// import { HttpClientModule } from '@angular/common/http';
// import { MatCardModule } from "@angular/material/card";
// import { MatToolbarModule } from "@angular/material/toolbar";
// import { MatButtonModule } from "@angular/material/button";
// import { MatIconModule } from '@angular/material/icon';
// import { MatInputModule} from '@angular/material/input';
// import { MatSelectModule} from '@angular/material/select';
// import { MatFormFieldModule } from '@angular/material/form-field';
// import { FlexLayoutModule } from "@angular/flex-layout";
// import { NgxEchartsModule } from 'ngx-echarts';
// import { AppComponent } from './app.component';
import { appConfig } from './app.config';
// import { HeaderComponent } from './components/header/header.component';
// import { CardComponent } from './components/card/card.component';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering()
  ]
};

export const config = mergeApplicationConfig(appConfig, serverConfig);

// @NgModule({
//   declarations: [
//     AppComponent, 
//     HeaderComponent,
//     CardComponent
//   ],
//   imports: [
//     BrowserModule,
//     FormsModule,
//     HttpClientModule,
//     BrowserAnimationsModule,
//     MatCardModule,
//     MatToolbarModule,
//     MatButtonModule,
//     MatIconModule,
//     MatFormFieldModule, 
//     MatSelectModule, 
//     MatInputModule,
//     FlexLayoutModule,
//     NgxEchartsModule.forRoot({
//       /**
//        * This will import all modules from echarts.
//        * If you only need custom modules,
//        * please refer to [Custom Build] section.
//        */
//       echarts: () => import('echarts'), // or import('./path-to-my-custom-echarts')
//     }),
//   ],
//   providers: [],
//   bootstrap: [AppComponent]
// })
// export class AppModule {
// }
