; ModuleID = 'etabackend/cpp/PARSE_TimeTagFileHeader.cpp'
source_filename = "etabackend/cpp/PARSE_TimeTagFileHeader.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct.header_info = type { i64, i64, i64, i64, i64, i64, i64 }
%struct.TgHd = type { [32 x i8], i32, i32, i64 }

@order_gurantee3 = dso_local global i64 0, align 8
@.str = private unnamed_addr constant [45 x i8] c"\0A [ERROR]Error when reading header, aborted.\00", align 1
@.str.1 = private unnamed_addr constant [41 x i8] c"\0A [ERROR]\0Aerror reading header, aborted.\00", align 1
@.str.2 = private unnamed_addr constant [7 x i8] c"%s(%d)\00", align 1
@.str.3 = private unnamed_addr constant [27 x i8] c"TTResultFormat_TTTRRecType\00", align 1
@.str.4 = private unnamed_addr constant [20 x i8] c"MeasDesc_Resolution\00", align 1
@.str.5 = private unnamed_addr constant [26 x i8] c"MeasDesc_GlobalResolution\00", align 1
@.str.6 = private unnamed_addr constant [3 x i32] [i32 37, i32 115, i32 0], align 4
@.str.7 = private unnamed_addr constant [11 x i8] c"Header_End\00", align 1
@.str.8 = private unnamed_addr constant [41 x i8] c"\0A [ERROR]Failed to read header, aborted.\00", align 1
@.str.9 = private unnamed_addr constant [7 x i8] c"PQTTTR\00", align 1
@.str.10 = private unnamed_addr constant [5 x i8] c"\87\B3\91\FA\00", align 1
@.str.11 = private unnamed_addr constant [93 x i8] c"\0A [ERROR]Unidentified time-tag format. Specify one the with eta.run(...format=x). Aborted. \0A\00", align 1

; Function Attrs: alwaysinline nounwind uwtable
define dso_local i64 @_Z5breadP11header_infoPvmmPc(%struct.header_info*, i8*, i64, i64, i8*) #0 {
  %6 = alloca %struct.header_info*, align 8
  %7 = alloca i8*, align 8
  %8 = alloca i64, align 8
  %9 = alloca i64, align 8
  %10 = alloca i8*, align 8
  store %struct.header_info* %0, %struct.header_info** %6, align 8
  store i8* %1, i8** %7, align 8
  store i64 %2, i64* %8, align 8
  store i64 %3, i64* %9, align 8
  store i8* %4, i8** %10, align 8
  %11 = load i8*, i8** %7, align 8
  %12 = load i8*, i8** %10, align 8
  %13 = load %struct.header_info*, %struct.header_info** %6, align 8
  %14 = getelementptr inbounds %struct.header_info, %struct.header_info* %13, i32 0, i32 1
  %15 = load i64, i64* %14, align 8
  %16 = getelementptr inbounds i8, i8* %12, i64 %15
  %17 = load i64, i64* %8, align 8
  %18 = load i64, i64* %9, align 8
  %19 = mul i64 %17, %18
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %11, i8* align 1 %16, i64 %19, i1 false)
  %20 = load i64, i64* %8, align 8
  %21 = load i64, i64* %9, align 8
  %22 = mul i64 %20, %21
  %23 = load %struct.header_info*, %struct.header_info** %6, align 8
  %24 = getelementptr inbounds %struct.header_info, %struct.header_info* %23, i32 0, i32 1
  %25 = load i64, i64* %24, align 8
  %26 = add i64 %25, %22
  store i64 %26, i64* %24, align 8
  %27 = load i64, i64* %8, align 8
  %28 = load i64, i64* %9, align 8
  %29 = mul i64 %27, %28
  ret i64 %29
}

; Function Attrs: argmemonly nounwind
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* nocapture writeonly, i8* nocapture readonly, i64, i1) #1

; Function Attrs: alwaysinline nounwind uwtable
define dso_local i32 @_Z23bh_4bytes_header_parserP11header_infoPc(%struct.header_info*, i8*) #0 {
  %3 = alloca %struct.header_info*, align 8
  %4 = alloca i8*, align 8
  store %struct.header_info* %0, %struct.header_info** %3, align 8
  store i8* %1, i8** %4, align 8
  %5 = load i8*, i8** %4, align 8
  %6 = bitcast i8* %5 to i16*
  %7 = getelementptr inbounds i16, i16* %6, i64 0
  %8 = load i16, i16* %7, align 2
  %9 = zext i16 %8 to i64
  %10 = load %struct.header_info*, %struct.header_info** %3, align 8
  %11 = getelementptr inbounds %struct.header_info, %struct.header_info* %10, i32 0, i32 4
  store i64 %9, i64* %11, align 8
  %12 = load %struct.header_info*, %struct.header_info** %3, align 8
  %13 = getelementptr inbounds %struct.header_info, %struct.header_info* %12, i32 0, i32 3
  store i64 1, i64* %13, align 8
  %14 = load %struct.header_info*, %struct.header_info** %3, align 8
  %15 = getelementptr inbounds %struct.header_info, %struct.header_info* %14, i32 0, i32 2
  store i64 0, i64* %15, align 8
  %16 = load %struct.header_info*, %struct.header_info** %3, align 8
  %17 = getelementptr inbounds %struct.header_info, %struct.header_info* %16, i32 0, i32 6
  store i64 3, i64* %17, align 8
  %18 = load %struct.header_info*, %struct.header_info** %3, align 8
  %19 = getelementptr inbounds %struct.header_info, %struct.header_info* %18, i32 0, i32 5
  store i64 4, i64* %19, align 8
  %20 = load %struct.header_info*, %struct.header_info** %3, align 8
  %21 = getelementptr inbounds %struct.header_info, %struct.header_info* %20, i32 0, i32 1
  store i64 4, i64* %21, align 8
  ret i32 0
}

; Function Attrs: alwaysinline nounwind uwtable
define dso_local i32 @_Z21Swebian_header_parserP11header_info(%struct.header_info*) #0 {
  %2 = alloca %struct.header_info*, align 8
  store %struct.header_info* %0, %struct.header_info** %2, align 8
  %3 = load %struct.header_info*, %struct.header_info** %2, align 8
  %4 = getelementptr inbounds %struct.header_info, %struct.header_info* %3, i32 0, i32 4
  store i64 0, i64* %4, align 8
  %5 = load %struct.header_info*, %struct.header_info** %2, align 8
  %6 = getelementptr inbounds %struct.header_info, %struct.header_info* %5, i32 0, i32 2
  store i64 1, i64* %6, align 8
  %7 = load %struct.header_info*, %struct.header_info** %2, align 8
  %8 = getelementptr inbounds %struct.header_info, %struct.header_info* %7, i32 0, i32 3
  store i64 1, i64* %8, align 8
  %9 = load %struct.header_info*, %struct.header_info** %2, align 8
  %10 = getelementptr inbounds %struct.header_info, %struct.header_info* %9, i32 0, i32 6
  store i64 1, i64* %10, align 8
  %11 = load %struct.header_info*, %struct.header_info** %2, align 8
  %12 = getelementptr inbounds %struct.header_info, %struct.header_info* %11, i32 0, i32 5
  store i64 16, i64* %12, align 8
  %13 = load %struct.header_info*, %struct.header_info** %2, align 8
  %14 = getelementptr inbounds %struct.header_info, %struct.header_info* %13, i32 0, i32 1
  store i64 0, i64* %14, align 8
  ret i32 0
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @_Z33quTAU_FORMAT_BINARY_header_parserP11header_infoPc(%struct.header_info*, i8*) #2 {
  %3 = alloca %struct.header_info*, align 8
  %4 = alloca i8*, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  %7 = alloca i8*, align 8
  %8 = alloca i32, align 4
  %9 = alloca %struct.header_info*, align 8
  %10 = alloca i8*, align 8
  %11 = alloca [32 x i8], align 16
  store %struct.header_info* %0, %struct.header_info** %9, align 8
  store i8* %1, i8** %10, align 8
  %12 = load %struct.header_info*, %struct.header_info** %9, align 8
  %13 = bitcast [32 x i8]* %11 to i8*
  %14 = load i8*, i8** %10, align 8
  store %struct.header_info* %12, %struct.header_info** %3, align 8
  store i8* %13, i8** %4, align 8
  store i64 1, i64* %5, align 8
  store i64 32, i64* %6, align 8
  store i8* %14, i8** %7, align 8
  %15 = load i8*, i8** %4, align 8
  %16 = load i8*, i8** %7, align 8
  %17 = load %struct.header_info*, %struct.header_info** %3, align 8
  %18 = getelementptr inbounds %struct.header_info, %struct.header_info* %17, i32 0, i32 1
  %19 = load i64, i64* %18, align 8
  %20 = getelementptr inbounds i8, i8* %16, i64 %19
  %21 = load i64, i64* %5, align 8
  %22 = load i64, i64* %6, align 8
  %23 = mul i64 %21, %22
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %15, i8* align 1 %20, i64 %23, i1 false) #7
  %24 = load i64, i64* %5, align 8
  %25 = load i64, i64* %6, align 8
  %26 = mul i64 %24, %25
  %27 = load %struct.header_info*, %struct.header_info** %3, align 8
  %28 = getelementptr inbounds %struct.header_info, %struct.header_info* %27, i32 0, i32 1
  %29 = load i64, i64* %28, align 8
  %30 = add i64 %29, %26
  store i64 %30, i64* %28, align 8
  %31 = load i64, i64* %5, align 8
  %32 = load i64, i64* %6, align 8
  %33 = mul i64 %31, %32
  %34 = icmp ne i64 %33, 32
  br i1 %34, label %35, label %38

; <label>:35:                                     ; preds = %2
  %36 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str, i32 0, i32 0))
  %37 = sext i32 %36 to i64
  store i64 %37, i64* @order_gurantee3, align 8
  store i32 -1, i32* %8, align 4
  br label %52

; <label>:38:                                     ; preds = %2
  %39 = load %struct.header_info*, %struct.header_info** %9, align 8
  %40 = getelementptr inbounds %struct.header_info, %struct.header_info* %39, i32 0, i32 6
  store i64 0, i64* %40, align 8
  %41 = load %struct.header_info*, %struct.header_info** %9, align 8
  %42 = getelementptr inbounds %struct.header_info, %struct.header_info* %41, i32 0, i32 5
  store i64 10, i64* %42, align 8
  %43 = load %struct.header_info*, %struct.header_info** %9, align 8
  %44 = getelementptr inbounds %struct.header_info, %struct.header_info* %43, i32 0, i32 2
  store i64 1, i64* %44, align 8
  %45 = load %struct.header_info*, %struct.header_info** %9, align 8
  %46 = getelementptr inbounds %struct.header_info, %struct.header_info* %45, i32 0, i32 2
  %47 = load i64, i64* %46, align 8
  %48 = load %struct.header_info*, %struct.header_info** %9, align 8
  %49 = getelementptr inbounds %struct.header_info, %struct.header_info* %48, i32 0, i32 3
  store i64 %47, i64* %49, align 8
  %50 = load %struct.header_info*, %struct.header_info** %9, align 8
  %51 = getelementptr inbounds %struct.header_info, %struct.header_info* %50, i32 0, i32 4
  store i64 1249, i64* %51, align 8
  store i32 0, i32* %8, align 4
  br label %52

; <label>:52:                                     ; preds = %38, %35
  %53 = load i32, i32* %8, align 4
  ret i32 %53
}

declare dso_local i32 @printf(i8*, ...) #3

; Function Attrs: alwaysinline uwtable
define dso_local i32 @_Z37quTAU_FORMAT_COMPRESSED_header_parserP11header_infoPc(%struct.header_info*, i8*) #2 {
  %3 = alloca %struct.header_info*, align 8
  %4 = alloca i8*, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  %7 = alloca i8*, align 8
  %8 = alloca i32, align 4
  %9 = alloca %struct.header_info*, align 8
  %10 = alloca i8*, align 8
  %11 = alloca [32 x i8], align 16
  store %struct.header_info* %0, %struct.header_info** %9, align 8
  store i8* %1, i8** %10, align 8
  %12 = load %struct.header_info*, %struct.header_info** %9, align 8
  %13 = bitcast [32 x i8]* %11 to i8*
  %14 = load i8*, i8** %10, align 8
  store %struct.header_info* %12, %struct.header_info** %3, align 8
  store i8* %13, i8** %4, align 8
  store i64 1, i64* %5, align 8
  store i64 32, i64* %6, align 8
  store i8* %14, i8** %7, align 8
  %15 = load i8*, i8** %4, align 8
  %16 = load i8*, i8** %7, align 8
  %17 = load %struct.header_info*, %struct.header_info** %3, align 8
  %18 = getelementptr inbounds %struct.header_info, %struct.header_info* %17, i32 0, i32 1
  %19 = load i64, i64* %18, align 8
  %20 = getelementptr inbounds i8, i8* %16, i64 %19
  %21 = load i64, i64* %5, align 8
  %22 = load i64, i64* %6, align 8
  %23 = mul i64 %21, %22
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %15, i8* align 1 %20, i64 %23, i1 false) #7
  %24 = load i64, i64* %5, align 8
  %25 = load i64, i64* %6, align 8
  %26 = mul i64 %24, %25
  %27 = load %struct.header_info*, %struct.header_info** %3, align 8
  %28 = getelementptr inbounds %struct.header_info, %struct.header_info* %27, i32 0, i32 1
  %29 = load i64, i64* %28, align 8
  %30 = add i64 %29, %26
  store i64 %30, i64* %28, align 8
  %31 = load i64, i64* %5, align 8
  %32 = load i64, i64* %6, align 8
  %33 = mul i64 %31, %32
  %34 = icmp ne i64 %33, 32
  br i1 %34, label %35, label %38

; <label>:35:                                     ; preds = %2
  %36 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str, i32 0, i32 0))
  %37 = sext i32 %36 to i64
  store i64 %37, i64* @order_gurantee3, align 8
  store i32 -1, i32* %8, align 4
  br label %52

; <label>:38:                                     ; preds = %2
  %39 = load %struct.header_info*, %struct.header_info** %9, align 8
  %40 = getelementptr inbounds %struct.header_info, %struct.header_info* %39, i32 0, i32 6
  store i64 0, i64* %40, align 8
  %41 = load %struct.header_info*, %struct.header_info** %9, align 8
  %42 = getelementptr inbounds %struct.header_info, %struct.header_info* %41, i32 0, i32 5
  store i64 5, i64* %42, align 8
  %43 = load %struct.header_info*, %struct.header_info** %9, align 8
  %44 = getelementptr inbounds %struct.header_info, %struct.header_info* %43, i32 0, i32 2
  store i64 1, i64* %44, align 8
  %45 = load %struct.header_info*, %struct.header_info** %9, align 8
  %46 = getelementptr inbounds %struct.header_info, %struct.header_info* %45, i32 0, i32 2
  %47 = load i64, i64* %46, align 8
  %48 = load %struct.header_info*, %struct.header_info** %9, align 8
  %49 = getelementptr inbounds %struct.header_info, %struct.header_info* %48, i32 0, i32 3
  store i64 %47, i64* %49, align 8
  %50 = load %struct.header_info*, %struct.header_info** %9, align 8
  %51 = getelementptr inbounds %struct.header_info, %struct.header_info* %50, i32 0, i32 4
  store i64 1249, i64* %51, align 8
  store i32 0, i32* %8, align 4
  br label %52

; <label>:52:                                     ; preds = %38, %35
  %53 = load i32, i32* %8, align 4
  ret i32 %53
}

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i64 @_Z15TDateTime_TimeTd(double) #4 {
  %2 = alloca double, align 8
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca i64, align 8
  store double %0, double* %2, align 8
  store i32 25569, i32* %3, align 4
  store i32 86400, i32* %4, align 4
  %6 = load double, double* %2, align 8
  %7 = fsub double %6, 2.556900e+04
  %8 = fmul double %7, 8.640000e+04
  %9 = fptosi double %8 to i64
  store i64 %9, i64* %5, align 8
  %10 = load i64, i64* %5, align 8
  ret i64 %10
}

; Function Attrs: alwaysinline uwtable
define dso_local i32 @_Z23PicoQuant_header_parserP11header_infoPc(%struct.header_info*, i8*) #2 {
  %3 = alloca %struct.header_info*, align 8
  %4 = alloca i8*, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  %7 = alloca i8*, align 8
  %8 = alloca %struct.header_info*, align 8
  %9 = alloca i8*, align 8
  %10 = alloca i64, align 8
  %11 = alloca i64, align 8
  %12 = alloca i8*, align 8
  %13 = alloca %struct.header_info*, align 8
  %14 = alloca i8*, align 8
  %15 = alloca i64, align 8
  %16 = alloca i64, align 8
  %17 = alloca i8*, align 8
  %18 = alloca %struct.header_info*, align 8
  %19 = alloca i8*, align 8
  %20 = alloca i64, align 8
  %21 = alloca i64, align 8
  %22 = alloca i8*, align 8
  %23 = alloca i32, align 4
  %24 = alloca %struct.header_info*, align 8
  %25 = alloca i8*, align 8
  %26 = alloca %struct.TgHd, align 8
  %27 = alloca i32, align 4
  %28 = alloca i8*, align 8
  %29 = alloca i32*, align 8
  %30 = alloca [8 x i8], align 1
  %31 = alloca [40 x i8], align 16
  %32 = alloca double, align 8
  %33 = alloca double, align 8
  %34 = alloca i64, align 8
  %35 = alloca i8, align 1
  store %struct.header_info* %0, %struct.header_info** %24, align 8
  store i8* %1, i8** %25, align 8
  %36 = load %struct.header_info*, %struct.header_info** %24, align 8
  %37 = bitcast [8 x i8]* %30 to i8*
  %38 = load i8*, i8** %25, align 8
  store %struct.header_info* %36, %struct.header_info** %18, align 8
  store i8* %37, i8** %19, align 8
  store i64 1, i64* %20, align 8
  store i64 8, i64* %21, align 8
  store i8* %38, i8** %22, align 8
  %39 = load i8*, i8** %19, align 8
  %40 = load i8*, i8** %22, align 8
  %41 = load %struct.header_info*, %struct.header_info** %18, align 8
  %42 = getelementptr inbounds %struct.header_info, %struct.header_info* %41, i32 0, i32 1
  %43 = load i64, i64* %42, align 8
  %44 = getelementptr inbounds i8, i8* %40, i64 %43
  %45 = load i64, i64* %20, align 8
  %46 = load i64, i64* %21, align 8
  %47 = mul i64 %45, %46
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %39, i8* align 1 %44, i64 %47, i1 false) #7
  %48 = load i64, i64* %20, align 8
  %49 = load i64, i64* %21, align 8
  %50 = mul i64 %48, %49
  %51 = load %struct.header_info*, %struct.header_info** %18, align 8
  %52 = getelementptr inbounds %struct.header_info, %struct.header_info* %51, i32 0, i32 1
  %53 = load i64, i64* %52, align 8
  %54 = add i64 %53, %50
  store i64 %54, i64* %52, align 8
  %55 = load i64, i64* %20, align 8
  %56 = load i64, i64* %21, align 8
  %57 = mul i64 %55, %56
  %58 = trunc i64 %57 to i32
  store i32 %58, i32* %27, align 4
  %59 = load i32, i32* %27, align 4
  %60 = sext i32 %59 to i64
  %61 = icmp ne i64 %60, 8
  br i1 %61, label %62, label %65

; <label>:62:                                     ; preds = %2
  %63 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @.str.1, i32 0, i32 0))
  %64 = sext i32 %63 to i64
  store i64 %64, i64* @order_gurantee3, align 8
  br label %289

; <label>:65:                                     ; preds = %2
  br label %66

; <label>:66:                                     ; preds = %254, %65
  %67 = load %struct.header_info*, %struct.header_info** %24, align 8
  %68 = bitcast %struct.TgHd* %26 to i8*
  %69 = load i8*, i8** %25, align 8
  store %struct.header_info* %67, %struct.header_info** %3, align 8
  store i8* %68, i8** %4, align 8
  store i64 1, i64* %5, align 8
  store i64 48, i64* %6, align 8
  store i8* %69, i8** %7, align 8
  %70 = load i8*, i8** %4, align 8
  %71 = load i8*, i8** %7, align 8
  %72 = load %struct.header_info*, %struct.header_info** %3, align 8
  %73 = getelementptr inbounds %struct.header_info, %struct.header_info* %72, i32 0, i32 1
  %74 = load i64, i64* %73, align 8
  %75 = getelementptr inbounds i8, i8* %71, i64 %74
  %76 = load i64, i64* %5, align 8
  %77 = load i64, i64* %6, align 8
  %78 = mul i64 %76, %77
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %70, i8* align 1 %75, i64 %78, i1 false) #7
  %79 = load i64, i64* %5, align 8
  %80 = load i64, i64* %6, align 8
  %81 = mul i64 %79, %80
  %82 = load %struct.header_info*, %struct.header_info** %3, align 8
  %83 = getelementptr inbounds %struct.header_info, %struct.header_info* %82, i32 0, i32 1
  %84 = load i64, i64* %83, align 8
  %85 = add i64 %84, %81
  store i64 %85, i64* %83, align 8
  %86 = load i64, i64* %5, align 8
  %87 = load i64, i64* %6, align 8
  %88 = mul i64 %86, %87
  %89 = trunc i64 %88 to i32
  store i32 %89, i32* %27, align 4
  %90 = load i32, i32* %27, align 4
  %91 = sext i32 %90 to i64
  %92 = icmp ne i64 %91, 48
  br i1 %92, label %93, label %94

; <label>:93:                                     ; preds = %66
  br label %289

; <label>:94:                                     ; preds = %66
  %95 = getelementptr inbounds [40 x i8], [40 x i8]* %31, i32 0, i32 0
  %96 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 0
  %97 = getelementptr inbounds [32 x i8], [32 x i8]* %96, i32 0, i32 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %95, i8* align 8 %97, i64 40, i1 false)
  %98 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 1
  %99 = load i32, i32* %98, align 8
  %100 = icmp sgt i32 %99, -1
  br i1 %100, label %101, label %108

; <label>:101:                                    ; preds = %94
  %102 = getelementptr inbounds [40 x i8], [40 x i8]* %31, i32 0, i32 0
  %103 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 0
  %104 = getelementptr inbounds [32 x i8], [32 x i8]* %103, i32 0, i32 0
  %105 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 1
  %106 = load i32, i32* %105, align 8
  %107 = call i32 (i8*, i8*, ...) @sprintf(i8* %102, i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.2, i32 0, i32 0), i8* %104, i32 %106) #7
  br label %108

; <label>:108:                                    ; preds = %101, %94
  %109 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 2
  %110 = load i32, i32* %109, align 4
  switch i32 %110, label %252 [
    i32 -65528, label %111
    i32 8, label %112
    i32 268435464, label %113
    i32 285212680, label %124
    i32 301989896, label %125
    i32 536870920, label %126
    i32 537001983, label %155
    i32 553648136, label %160
    i32 1073872895, label %165
    i32 1073938431, label %203
    i32 -1, label %247
  ]

; <label>:111:                                    ; preds = %108
  br label %253

; <label>:112:                                    ; preds = %108
  br label %253

; <label>:113:                                    ; preds = %108
  %114 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 0
  %115 = getelementptr inbounds [32 x i8], [32 x i8]* %114, i32 0, i32 0
  %116 = call i32 @strcmp(i8* %115, i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str.3, i32 0, i32 0)) #8
  %117 = icmp eq i32 %116, 0
  br i1 %117, label %118, label %123

; <label>:118:                                    ; preds = %113
  %119 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %120 = load i64, i64* %119, align 8
  %121 = load %struct.header_info*, %struct.header_info** %24, align 8
  %122 = getelementptr inbounds %struct.header_info, %struct.header_info* %121, i32 0, i32 6
  store i64 %120, i64* %122, align 8
  br label %123

; <label>:123:                                    ; preds = %118, %113
  br label %253

; <label>:124:                                    ; preds = %108
  br label %253

; <label>:125:                                    ; preds = %108
  br label %253

; <label>:126:                                    ; preds = %108
  %127 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 0
  %128 = getelementptr inbounds [32 x i8], [32 x i8]* %127, i32 0, i32 0
  %129 = call i32 @strcmp(i8* %128, i8* getelementptr inbounds ([20 x i8], [20 x i8]* @.str.4, i32 0, i32 0)) #8
  %130 = icmp eq i32 %129, 0
  br i1 %130, label %131, label %140

; <label>:131:                                    ; preds = %126
  %132 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %133 = bitcast i64* %132 to double*
  %134 = load double, double* %133, align 8
  store double %134, double* %32, align 8
  %135 = load double, double* %32, align 8
  %136 = fmul double %135, 1.000000e+12
  %137 = fptosi double %136 to i64
  %138 = load %struct.header_info*, %struct.header_info** %24, align 8
  %139 = getelementptr inbounds %struct.header_info, %struct.header_info* %138, i32 0, i32 3
  store i64 %137, i64* %139, align 8
  br label %140

; <label>:140:                                    ; preds = %131, %126
  %141 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 0
  %142 = getelementptr inbounds [32 x i8], [32 x i8]* %141, i32 0, i32 0
  %143 = call i32 @strcmp(i8* %142, i8* getelementptr inbounds ([26 x i8], [26 x i8]* @.str.5, i32 0, i32 0)) #8
  %144 = icmp eq i32 %143, 0
  br i1 %144, label %145, label %154

; <label>:145:                                    ; preds = %140
  %146 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %147 = bitcast i64* %146 to double*
  %148 = load double, double* %147, align 8
  store double %148, double* %33, align 8
  %149 = load double, double* %33, align 8
  %150 = fmul double %149, 1.000000e+12
  %151 = fptosi double %150 to i64
  %152 = load %struct.header_info*, %struct.header_info** %24, align 8
  %153 = getelementptr inbounds %struct.header_info, %struct.header_info* %152, i32 0, i32 2
  store i64 %151, i64* %153, align 8
  br label %154

; <label>:154:                                    ; preds = %145, %140
  br label %253

; <label>:155:                                    ; preds = %108
  %156 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %157 = load i64, i64* %156, align 8
  %158 = load %struct.header_info*, %struct.header_info** %24, align 8
  %159 = getelementptr inbounds %struct.header_info, %struct.header_info* %158, i32 0, i32 1
  store i64 %157, i64* %159, align 8
  br label %253

; <label>:160:                                    ; preds = %108
  %161 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %162 = bitcast i64* %161 to double*
  %163 = load double, double* %162, align 8
  %164 = call i64 @_Z15TDateTime_TimeTd(double %163)
  store i64 %164, i64* %34, align 8
  br label %253

; <label>:165:                                    ; preds = %108
  %166 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %167 = load i64, i64* %166, align 8
  %168 = call noalias i8* @calloc(i64 %167, i64 1) #7
  store i8* %168, i8** %28, align 8
  %169 = load %struct.header_info*, %struct.header_info** %24, align 8
  %170 = load i8*, i8** %28, align 8
  %171 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %172 = load i64, i64* %171, align 8
  %173 = load i8*, i8** %25, align 8
  store %struct.header_info* %169, %struct.header_info** %8, align 8
  store i8* %170, i8** %9, align 8
  store i64 1, i64* %10, align 8
  store i64 %172, i64* %11, align 8
  store i8* %173, i8** %12, align 8
  %174 = load i8*, i8** %9, align 8
  %175 = load i8*, i8** %12, align 8
  %176 = load %struct.header_info*, %struct.header_info** %8, align 8
  %177 = getelementptr inbounds %struct.header_info, %struct.header_info* %176, i32 0, i32 1
  %178 = load i64, i64* %177, align 8
  %179 = getelementptr inbounds i8, i8* %175, i64 %178
  %180 = load i64, i64* %10, align 8
  %181 = load i64, i64* %11, align 8
  %182 = mul i64 %180, %181
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %174, i8* align 1 %179, i64 %182, i1 false) #7
  %183 = load i64, i64* %10, align 8
  %184 = load i64, i64* %11, align 8
  %185 = mul i64 %183, %184
  %186 = load %struct.header_info*, %struct.header_info** %8, align 8
  %187 = getelementptr inbounds %struct.header_info, %struct.header_info* %186, i32 0, i32 1
  %188 = load i64, i64* %187, align 8
  %189 = add i64 %188, %185
  store i64 %189, i64* %187, align 8
  %190 = load i64, i64* %10, align 8
  %191 = load i64, i64* %11, align 8
  %192 = mul i64 %190, %191
  %193 = trunc i64 %192 to i32
  store i32 %193, i32* %27, align 4
  %194 = load i32, i32* %27, align 4
  %195 = sext i32 %194 to i64
  %196 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %197 = load i64, i64* %196, align 8
  %198 = icmp ne i64 %195, %197
  br i1 %198, label %199, label %201

; <label>:199:                                    ; preds = %165
  %200 = load i8*, i8** %28, align 8
  call void @free(i8* %200) #7
  br label %289

; <label>:201:                                    ; preds = %165
  %202 = load i8*, i8** %28, align 8
  call void @free(i8* %202) #7
  br label %253

; <label>:203:                                    ; preds = %108
  %204 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %205 = load i64, i64* %204, align 8
  %206 = call noalias i8* @calloc(i64 %205, i64 1) #7
  %207 = bitcast i8* %206 to i32*
  store i32* %207, i32** %29, align 8
  %208 = load %struct.header_info*, %struct.header_info** %24, align 8
  %209 = load i32*, i32** %29, align 8
  %210 = bitcast i32* %209 to i8*
  %211 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %212 = load i64, i64* %211, align 8
  %213 = load i8*, i8** %25, align 8
  store %struct.header_info* %208, %struct.header_info** %13, align 8
  store i8* %210, i8** %14, align 8
  store i64 1, i64* %15, align 8
  store i64 %212, i64* %16, align 8
  store i8* %213, i8** %17, align 8
  %214 = load i8*, i8** %14, align 8
  %215 = load i8*, i8** %17, align 8
  %216 = load %struct.header_info*, %struct.header_info** %13, align 8
  %217 = getelementptr inbounds %struct.header_info, %struct.header_info* %216, i32 0, i32 1
  %218 = load i64, i64* %217, align 8
  %219 = getelementptr inbounds i8, i8* %215, i64 %218
  %220 = load i64, i64* %15, align 8
  %221 = load i64, i64* %16, align 8
  %222 = mul i64 %220, %221
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %214, i8* align 1 %219, i64 %222, i1 false) #7
  %223 = load i64, i64* %15, align 8
  %224 = load i64, i64* %16, align 8
  %225 = mul i64 %223, %224
  %226 = load %struct.header_info*, %struct.header_info** %13, align 8
  %227 = getelementptr inbounds %struct.header_info, %struct.header_info* %226, i32 0, i32 1
  %228 = load i64, i64* %227, align 8
  %229 = add i64 %228, %225
  store i64 %229, i64* %227, align 8
  %230 = load i64, i64* %15, align 8
  %231 = load i64, i64* %16, align 8
  %232 = mul i64 %230, %231
  %233 = trunc i64 %232 to i32
  store i32 %233, i32* %27, align 4
  %234 = load i32, i32* %27, align 4
  %235 = sext i32 %234 to i64
  %236 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %237 = load i64, i64* %236, align 8
  %238 = icmp ne i64 %235, %237
  br i1 %238, label %239, label %242

; <label>:239:                                    ; preds = %203
  %240 = load i32*, i32** %29, align 8
  %241 = bitcast i32* %240 to i8*
  call void @free(i8* %241) #7
  br label %289

; <label>:242:                                    ; preds = %203
  %243 = load i32*, i32** %29, align 8
  %244 = call i32 (i32*, ...) @wprintf(i32* getelementptr inbounds ([3 x i32], [3 x i32]* @.str.6, i32 0, i32 0), i32* %243)
  %245 = load i32*, i32** %29, align 8
  %246 = bitcast i32* %245 to i8*
  call void @free(i8* %246) #7
  br label %253

; <label>:247:                                    ; preds = %108
  %248 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 3
  %249 = load i64, i64* %248, align 8
  %250 = load %struct.header_info*, %struct.header_info** %24, align 8
  %251 = getelementptr inbounds %struct.header_info, %struct.header_info* %250, i32 0, i32 1
  store i64 %249, i64* %251, align 8
  br label %253

; <label>:252:                                    ; preds = %108
  br label %289

; <label>:253:                                    ; preds = %247, %242, %201, %160, %155, %154, %125, %124, %123, %112, %111
  br label %254

; <label>:254:                                    ; preds = %253
  %255 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %26, i32 0, i32 0
  %256 = getelementptr inbounds [32 x i8], [32 x i8]* %255, i32 0, i32 0
  %257 = call i32 @strncmp(i8* %256, i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.7, i32 0, i32 0), i64 11) #8
  %258 = icmp ne i32 %257, 0
  br i1 %258, label %66, label %259

; <label>:259:                                    ; preds = %254
  %260 = load %struct.header_info*, %struct.header_info** %24, align 8
  %261 = getelementptr inbounds %struct.header_info, %struct.header_info* %260, i32 0, i32 6
  %262 = load i64, i64* %261, align 8
  switch i64 %262, label %273 [
    i64 66051, label %263
    i64 66052, label %264
    i64 16843268, label %265
    i64 66053, label %266
    i64 66054, label %267
    i64 66307, label %268
    i64 66308, label %269
    i64 16843524, label %270
    i64 66309, label %271
    i64 66310, label %272
  ]

; <label>:263:                                    ; preds = %259
  store i8 1, i8* %35, align 1
  br label %274

; <label>:264:                                    ; preds = %259
  store i8 1, i8* %35, align 1
  br label %274

; <label>:265:                                    ; preds = %259
  store i8 1, i8* %35, align 1
  br label %274

; <label>:266:                                    ; preds = %259
  store i8 1, i8* %35, align 1
  br label %274

; <label>:267:                                    ; preds = %259
  store i8 1, i8* %35, align 1
  br label %274

; <label>:268:                                    ; preds = %259
  store i8 0, i8* %35, align 1
  br label %274

; <label>:269:                                    ; preds = %259
  store i8 0, i8* %35, align 1
  br label %274

; <label>:270:                                    ; preds = %259
  store i8 0, i8* %35, align 1
  br label %274

; <label>:271:                                    ; preds = %259
  store i8 0, i8* %35, align 1
  br label %274

; <label>:272:                                    ; preds = %259
  store i8 0, i8* %35, align 1
  br label %274

; <label>:273:                                    ; preds = %259
  br label %289

; <label>:274:                                    ; preds = %272, %271, %270, %269, %268, %267, %266, %265, %264, %263
  %275 = load i8, i8* %35, align 1
  %276 = trunc i8 %275 to i1
  br i1 %276, label %277, label %280

; <label>:277:                                    ; preds = %274
  %278 = load %struct.header_info*, %struct.header_info** %24, align 8
  %279 = getelementptr inbounds %struct.header_info, %struct.header_info* %278, i32 0, i32 4
  store i64 1, i64* %279, align 8
  br label %286

; <label>:280:                                    ; preds = %274
  %281 = load %struct.header_info*, %struct.header_info** %24, align 8
  %282 = getelementptr inbounds %struct.header_info, %struct.header_info* %281, i32 0, i32 2
  %283 = load i64, i64* %282, align 8
  %284 = load %struct.header_info*, %struct.header_info** %24, align 8
  %285 = getelementptr inbounds %struct.header_info, %struct.header_info* %284, i32 0, i32 4
  store i64 %283, i64* %285, align 8
  br label %286

; <label>:286:                                    ; preds = %280, %277
  %287 = load %struct.header_info*, %struct.header_info** %24, align 8
  %288 = getelementptr inbounds %struct.header_info, %struct.header_info* %287, i32 0, i32 5
  store i64 4, i64* %288, align 8
  store i32 0, i32* %23, align 4
  br label %291

; <label>:289:                                    ; preds = %273, %252, %239, %199, %93, %62
  store i32 -1, i32* %23, align 4
  br label %291
                                                  ; No predecessors!
  store i32 -2, i32* %23, align 4
  br label %291

; <label>:291:                                    ; preds = %290, %289, %286
  %292 = load i32, i32* %23, align 4
  ret i32 %292
}

; Function Attrs: nounwind
declare dso_local i32 @sprintf(i8*, i8*, ...) #5

; Function Attrs: nounwind readonly
declare dso_local i32 @strcmp(i8*, i8*) #6

; Function Attrs: nounwind
declare dso_local noalias i8* @calloc(i64, i64) #5

; Function Attrs: nounwind
declare dso_local void @free(i8*) #5

declare dso_local i32 @wprintf(i32*, ...) #3

; Function Attrs: nounwind readonly
declare dso_local i32 @strncmp(i8*, i8*, i64) #6

; Function Attrs: alwaysinline uwtable
define dso_local i32 @PARSE_TimeTagFileHeader(%struct.header_info*, i8*) #2 {
  %3 = alloca %struct.header_info*, align 8
  %4 = alloca i8*, align 8
  %5 = alloca %struct.header_info*, align 8
  %6 = alloca i8*, align 8
  %7 = alloca i64, align 8
  %8 = alloca i64, align 8
  %9 = alloca i8*, align 8
  %10 = alloca i32, align 4
  %11 = alloca %struct.header_info*, align 8
  %12 = alloca i8*, align 8
  %13 = alloca %struct.header_info*, align 8
  %14 = alloca %struct.header_info*, align 8
  %15 = alloca i8*, align 8
  %16 = alloca i64, align 8
  %17 = alloca i64, align 8
  %18 = alloca i8*, align 8
  %19 = alloca i32, align 4
  %20 = alloca %struct.header_info*, align 8
  %21 = alloca i8*, align 8
  %22 = alloca [32 x i8], align 16
  %23 = alloca %struct.header_info*, align 8
  %24 = alloca i8*, align 8
  %25 = alloca i64, align 8
  %26 = alloca i64, align 8
  %27 = alloca i8*, align 8
  %28 = alloca %struct.header_info*, align 8
  %29 = alloca i8*, align 8
  %30 = alloca i64, align 8
  %31 = alloca i64, align 8
  %32 = alloca i8*, align 8
  %33 = alloca %struct.header_info*, align 8
  %34 = alloca i8*, align 8
  %35 = alloca i64, align 8
  %36 = alloca i64, align 8
  %37 = alloca i8*, align 8
  %38 = alloca %struct.header_info*, align 8
  %39 = alloca i8*, align 8
  %40 = alloca i64, align 8
  %41 = alloca i64, align 8
  %42 = alloca i8*, align 8
  %43 = alloca i32, align 4
  %44 = alloca %struct.header_info*, align 8
  %45 = alloca i8*, align 8
  %46 = alloca %struct.TgHd, align 8
  %47 = alloca i32, align 4
  %48 = alloca i8*, align 8
  %49 = alloca i32*, align 8
  %50 = alloca [8 x i8], align 1
  %51 = alloca [40 x i8], align 16
  %52 = alloca double, align 8
  %53 = alloca double, align 8
  %54 = alloca i64, align 8
  %55 = alloca i8, align 1
  %56 = alloca %struct.header_info*, align 8
  %57 = alloca i8*, align 8
  %58 = alloca i64, align 8
  %59 = alloca i64, align 8
  %60 = alloca i8*, align 8
  %61 = alloca i32, align 4
  %62 = alloca %struct.header_info*, align 8
  %63 = alloca i8*, align 8
  %64 = alloca i32, align 4
  %65 = alloca [8 x i8], align 1
  %66 = alloca i8, align 1
  store %struct.header_info* %0, %struct.header_info** %62, align 8
  store i8* %1, i8** %63, align 8
  store i32 -1, i32* %64, align 4
  %67 = load %struct.header_info*, %struct.header_info** %62, align 8
  %68 = getelementptr inbounds %struct.header_info, %struct.header_info* %67, i32 0, i32 1
  store i64 0, i64* %68, align 8
  %69 = load %struct.header_info*, %struct.header_info** %62, align 8
  %70 = bitcast [8 x i8]* %65 to i8*
  %71 = load i8*, i8** %63, align 8
  store %struct.header_info* %69, %struct.header_info** %56, align 8
  store i8* %70, i8** %57, align 8
  store i64 1, i64* %58, align 8
  store i64 8, i64* %59, align 8
  store i8* %71, i8** %60, align 8
  %72 = load i8*, i8** %57, align 8
  %73 = load i8*, i8** %60, align 8
  %74 = load %struct.header_info*, %struct.header_info** %56, align 8
  %75 = getelementptr inbounds %struct.header_info, %struct.header_info* %74, i32 0, i32 1
  %76 = load i64, i64* %75, align 8
  %77 = getelementptr inbounds i8, i8* %73, i64 %76
  %78 = load i64, i64* %58, align 8
  %79 = load i64, i64* %59, align 8
  %80 = mul i64 %78, %79
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %72, i8* align 1 %77, i64 %80, i1 false) #7
  %81 = load i64, i64* %58, align 8
  %82 = load i64, i64* %59, align 8
  %83 = mul i64 %81, %82
  %84 = load %struct.header_info*, %struct.header_info** %56, align 8
  %85 = getelementptr inbounds %struct.header_info, %struct.header_info* %84, i32 0, i32 1
  %86 = load i64, i64* %85, align 8
  %87 = add i64 %86, %83
  store i64 %87, i64* %85, align 8
  %88 = load i64, i64* %58, align 8
  %89 = load i64, i64* %59, align 8
  %90 = mul i64 %88, %89
  %91 = icmp ne i64 %90, 8
  br i1 %91, label %92, label %95

; <label>:92:                                     ; preds = %2
  %93 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @.str.8, i32 0, i32 0))
  %94 = sext i32 %93 to i64
  store i64 %94, i64* @order_gurantee3, align 8
  store i32 -2, i32* %61, align 4
  br label %512

; <label>:95:                                     ; preds = %2
  store i8 1, i8* %66, align 1
  %96 = load %struct.header_info*, %struct.header_info** %62, align 8
  %97 = getelementptr inbounds %struct.header_info, %struct.header_info* %96, i32 0, i32 6
  %98 = load i64, i64* %97, align 8
  %99 = icmp eq i64 %98, -1
  br i1 %99, label %100, label %115

; <label>:100:                                    ; preds = %95
  %101 = getelementptr inbounds [8 x i8], [8 x i8]* %65, i32 0, i32 0
  %102 = call i32 @strncmp(i8* %101, i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.9, i32 0, i32 0), i64 6) #8
  %103 = icmp eq i32 %102, 0
  br i1 %103, label %104, label %107

; <label>:104:                                    ; preds = %100
  %105 = load %struct.header_info*, %struct.header_info** %62, align 8
  %106 = getelementptr inbounds %struct.header_info, %struct.header_info* %105, i32 0, i32 6
  store i64 4, i64* %106, align 8
  br label %107

; <label>:107:                                    ; preds = %104, %100
  %108 = getelementptr inbounds [8 x i8], [8 x i8]* %65, i32 0, i32 0
  %109 = call i32 @strncmp(i8* %108, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.10, i32 0, i32 0), i64 4) #8
  %110 = icmp eq i32 %109, 0
  br i1 %110, label %111, label %114

; <label>:111:                                    ; preds = %107
  %112 = load %struct.header_info*, %struct.header_info** %62, align 8
  %113 = getelementptr inbounds %struct.header_info, %struct.header_info* %112, i32 0, i32 6
  store i64 0, i64* %113, align 8
  br label %114

; <label>:114:                                    ; preds = %111, %107
  br label %115

; <label>:115:                                    ; preds = %114, %95
  %116 = load %struct.header_info*, %struct.header_info** %62, align 8
  %117 = getelementptr inbounds %struct.header_info, %struct.header_info* %116, i32 0, i32 6
  %118 = load i64, i64* %117, align 8
  switch i64 %118, label %505 [
    i64 0, label %119
    i64 1, label %164
    i64 2, label %178
    i64 3, label %223
    i64 4, label %242
    i64 -1, label %500
  ]

; <label>:119:                                    ; preds = %115
  %120 = load %struct.header_info*, %struct.header_info** %62, align 8
  %121 = load i8*, i8** %63, align 8
  store %struct.header_info* %120, %struct.header_info** %20, align 8
  store i8* %121, i8** %21, align 8
  %122 = load %struct.header_info*, %struct.header_info** %20, align 8
  %123 = bitcast [32 x i8]* %22 to i8*
  %124 = load i8*, i8** %21, align 8
  store %struct.header_info* %122, %struct.header_info** %14, align 8
  store i8* %123, i8** %15, align 8
  store i64 1, i64* %16, align 8
  store i64 32, i64* %17, align 8
  store i8* %124, i8** %18, align 8
  %125 = load i8*, i8** %15, align 8
  %126 = load i8*, i8** %18, align 8
  %127 = load %struct.header_info*, %struct.header_info** %14, align 8
  %128 = getelementptr inbounds %struct.header_info, %struct.header_info* %127, i32 0, i32 1
  %129 = load i64, i64* %128, align 8
  %130 = getelementptr inbounds i8, i8* %126, i64 %129
  %131 = load i64, i64* %16, align 8
  %132 = load i64, i64* %17, align 8
  %133 = mul i64 %131, %132
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %125, i8* align 1 %130, i64 %133, i1 false) #7
  %134 = load i64, i64* %16, align 8
  %135 = load i64, i64* %17, align 8
  %136 = mul i64 %134, %135
  %137 = load %struct.header_info*, %struct.header_info** %14, align 8
  %138 = getelementptr inbounds %struct.header_info, %struct.header_info* %137, i32 0, i32 1
  %139 = load i64, i64* %138, align 8
  %140 = add i64 %139, %136
  store i64 %140, i64* %138, align 8
  %141 = load i64, i64* %16, align 8
  %142 = load i64, i64* %17, align 8
  %143 = mul i64 %141, %142
  %144 = icmp ne i64 %143, 32
  br i1 %144, label %145, label %148

; <label>:145:                                    ; preds = %119
  %146 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str, i32 0, i32 0))
  %147 = sext i32 %146 to i64
  store i64 %147, i64* @order_gurantee3, align 8
  store i32 -1, i32* %19, align 4
  br label %162

; <label>:148:                                    ; preds = %119
  %149 = load %struct.header_info*, %struct.header_info** %20, align 8
  %150 = getelementptr inbounds %struct.header_info, %struct.header_info* %149, i32 0, i32 6
  store i64 0, i64* %150, align 8
  %151 = load %struct.header_info*, %struct.header_info** %20, align 8
  %152 = getelementptr inbounds %struct.header_info, %struct.header_info* %151, i32 0, i32 5
  store i64 10, i64* %152, align 8
  %153 = load %struct.header_info*, %struct.header_info** %20, align 8
  %154 = getelementptr inbounds %struct.header_info, %struct.header_info* %153, i32 0, i32 2
  store i64 1, i64* %154, align 8
  %155 = load %struct.header_info*, %struct.header_info** %20, align 8
  %156 = getelementptr inbounds %struct.header_info, %struct.header_info* %155, i32 0, i32 2
  %157 = load i64, i64* %156, align 8
  %158 = load %struct.header_info*, %struct.header_info** %20, align 8
  %159 = getelementptr inbounds %struct.header_info, %struct.header_info* %158, i32 0, i32 3
  store i64 %157, i64* %159, align 8
  %160 = load %struct.header_info*, %struct.header_info** %20, align 8
  %161 = getelementptr inbounds %struct.header_info, %struct.header_info* %160, i32 0, i32 4
  store i64 1249, i64* %161, align 8
  store i32 0, i32* %19, align 4
  br label %162

; <label>:162:                                    ; preds = %145, %148
  %163 = load i32, i32* %19, align 4
  store i32 %163, i32* %64, align 4
  br label %505

; <label>:164:                                    ; preds = %115
  %165 = load %struct.header_info*, %struct.header_info** %62, align 8
  store %struct.header_info* %165, %struct.header_info** %13, align 8
  %166 = load %struct.header_info*, %struct.header_info** %13, align 8
  %167 = getelementptr inbounds %struct.header_info, %struct.header_info* %166, i32 0, i32 4
  store i64 0, i64* %167, align 8
  %168 = load %struct.header_info*, %struct.header_info** %13, align 8
  %169 = getelementptr inbounds %struct.header_info, %struct.header_info* %168, i32 0, i32 2
  store i64 1, i64* %169, align 8
  %170 = load %struct.header_info*, %struct.header_info** %13, align 8
  %171 = getelementptr inbounds %struct.header_info, %struct.header_info* %170, i32 0, i32 3
  store i64 1, i64* %171, align 8
  %172 = load %struct.header_info*, %struct.header_info** %13, align 8
  %173 = getelementptr inbounds %struct.header_info, %struct.header_info* %172, i32 0, i32 6
  store i64 1, i64* %173, align 8
  %174 = load %struct.header_info*, %struct.header_info** %13, align 8
  %175 = getelementptr inbounds %struct.header_info, %struct.header_info* %174, i32 0, i32 5
  store i64 16, i64* %175, align 8
  %176 = load %struct.header_info*, %struct.header_info** %13, align 8
  %177 = getelementptr inbounds %struct.header_info, %struct.header_info* %176, i32 0, i32 1
  store i64 0, i64* %177, align 8
  store i32 0, i32* %64, align 4
  br label %505

; <label>:178:                                    ; preds = %115
  %179 = load %struct.header_info*, %struct.header_info** %62, align 8
  %180 = load i8*, i8** %63, align 8
  store %struct.header_info* %179, %struct.header_info** %11, align 8
  store i8* %180, i8** %12, align 8
  %181 = load %struct.header_info*, %struct.header_info** %11, align 8
  %182 = bitcast [32 x i8]* %22 to i8*
  %183 = load i8*, i8** %12, align 8
  store %struct.header_info* %181, %struct.header_info** %5, align 8
  store i8* %182, i8** %6, align 8
  store i64 1, i64* %7, align 8
  store i64 32, i64* %8, align 8
  store i8* %183, i8** %9, align 8
  %184 = load i8*, i8** %6, align 8
  %185 = load i8*, i8** %9, align 8
  %186 = load %struct.header_info*, %struct.header_info** %5, align 8
  %187 = getelementptr inbounds %struct.header_info, %struct.header_info* %186, i32 0, i32 1
  %188 = load i64, i64* %187, align 8
  %189 = getelementptr inbounds i8, i8* %185, i64 %188
  %190 = load i64, i64* %7, align 8
  %191 = load i64, i64* %8, align 8
  %192 = mul i64 %190, %191
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %184, i8* align 1 %189, i64 %192, i1 false) #7
  %193 = load i64, i64* %7, align 8
  %194 = load i64, i64* %8, align 8
  %195 = mul i64 %193, %194
  %196 = load %struct.header_info*, %struct.header_info** %5, align 8
  %197 = getelementptr inbounds %struct.header_info, %struct.header_info* %196, i32 0, i32 1
  %198 = load i64, i64* %197, align 8
  %199 = add i64 %198, %195
  store i64 %199, i64* %197, align 8
  %200 = load i64, i64* %7, align 8
  %201 = load i64, i64* %8, align 8
  %202 = mul i64 %200, %201
  %203 = icmp ne i64 %202, 32
  br i1 %203, label %204, label %207

; <label>:204:                                    ; preds = %178
  %205 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([45 x i8], [45 x i8]* @.str, i32 0, i32 0))
  %206 = sext i32 %205 to i64
  store i64 %206, i64* @order_gurantee3, align 8
  store i32 -1, i32* %10, align 4
  br label %221

; <label>:207:                                    ; preds = %178
  %208 = load %struct.header_info*, %struct.header_info** %11, align 8
  %209 = getelementptr inbounds %struct.header_info, %struct.header_info* %208, i32 0, i32 6
  store i64 0, i64* %209, align 8
  %210 = load %struct.header_info*, %struct.header_info** %11, align 8
  %211 = getelementptr inbounds %struct.header_info, %struct.header_info* %210, i32 0, i32 5
  store i64 5, i64* %211, align 8
  %212 = load %struct.header_info*, %struct.header_info** %11, align 8
  %213 = getelementptr inbounds %struct.header_info, %struct.header_info* %212, i32 0, i32 2
  store i64 1, i64* %213, align 8
  %214 = load %struct.header_info*, %struct.header_info** %11, align 8
  %215 = getelementptr inbounds %struct.header_info, %struct.header_info* %214, i32 0, i32 2
  %216 = load i64, i64* %215, align 8
  %217 = load %struct.header_info*, %struct.header_info** %11, align 8
  %218 = getelementptr inbounds %struct.header_info, %struct.header_info* %217, i32 0, i32 3
  store i64 %216, i64* %218, align 8
  %219 = load %struct.header_info*, %struct.header_info** %11, align 8
  %220 = getelementptr inbounds %struct.header_info, %struct.header_info* %219, i32 0, i32 4
  store i64 1249, i64* %220, align 8
  store i32 0, i32* %10, align 4
  br label %221

; <label>:221:                                    ; preds = %204, %207
  %222 = load i32, i32* %10, align 4
  store i32 %222, i32* %64, align 4
  br label %505

; <label>:223:                                    ; preds = %115
  %224 = load %struct.header_info*, %struct.header_info** %62, align 8
  %225 = getelementptr inbounds [8 x i8], [8 x i8]* %65, i32 0, i32 0
  store %struct.header_info* %224, %struct.header_info** %3, align 8
  store i8* %225, i8** %4, align 8
  %226 = load i8*, i8** %4, align 8
  %227 = bitcast i8* %226 to i16*
  %228 = load i16, i16* %227, align 2
  %229 = zext i16 %228 to i64
  %230 = load %struct.header_info*, %struct.header_info** %3, align 8
  %231 = getelementptr inbounds %struct.header_info, %struct.header_info* %230, i32 0, i32 4
  store i64 %229, i64* %231, align 8
  %232 = load %struct.header_info*, %struct.header_info** %3, align 8
  %233 = getelementptr inbounds %struct.header_info, %struct.header_info* %232, i32 0, i32 3
  store i64 1, i64* %233, align 8
  %234 = load %struct.header_info*, %struct.header_info** %3, align 8
  %235 = getelementptr inbounds %struct.header_info, %struct.header_info* %234, i32 0, i32 2
  store i64 0, i64* %235, align 8
  %236 = load %struct.header_info*, %struct.header_info** %3, align 8
  %237 = getelementptr inbounds %struct.header_info, %struct.header_info* %236, i32 0, i32 6
  store i64 3, i64* %237, align 8
  %238 = load %struct.header_info*, %struct.header_info** %3, align 8
  %239 = getelementptr inbounds %struct.header_info, %struct.header_info* %238, i32 0, i32 5
  store i64 4, i64* %239, align 8
  %240 = load %struct.header_info*, %struct.header_info** %3, align 8
  %241 = getelementptr inbounds %struct.header_info, %struct.header_info* %240, i32 0, i32 1
  store i64 4, i64* %241, align 8
  store i32 0, i32* %64, align 4
  br label %505

; <label>:242:                                    ; preds = %115
  %243 = load %struct.header_info*, %struct.header_info** %62, align 8
  %244 = load i8*, i8** %63, align 8
  store %struct.header_info* %243, %struct.header_info** %44, align 8
  store i8* %244, i8** %45, align 8
  %245 = load %struct.header_info*, %struct.header_info** %44, align 8
  %246 = bitcast [8 x i8]* %50 to i8*
  %247 = load i8*, i8** %45, align 8
  store %struct.header_info* %245, %struct.header_info** %38, align 8
  store i8* %246, i8** %39, align 8
  store i64 1, i64* %40, align 8
  store i64 8, i64* %41, align 8
  store i8* %247, i8** %42, align 8
  %248 = load i8*, i8** %39, align 8
  %249 = load i8*, i8** %42, align 8
  %250 = load %struct.header_info*, %struct.header_info** %38, align 8
  %251 = getelementptr inbounds %struct.header_info, %struct.header_info* %250, i32 0, i32 1
  %252 = load i64, i64* %251, align 8
  %253 = getelementptr inbounds i8, i8* %249, i64 %252
  %254 = load i64, i64* %40, align 8
  %255 = load i64, i64* %41, align 8
  %256 = mul i64 %254, %255
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %248, i8* align 1 %253, i64 %256, i1 false) #7
  %257 = load i64, i64* %40, align 8
  %258 = load i64, i64* %41, align 8
  %259 = mul i64 %257, %258
  %260 = load %struct.header_info*, %struct.header_info** %38, align 8
  %261 = getelementptr inbounds %struct.header_info, %struct.header_info* %260, i32 0, i32 1
  %262 = load i64, i64* %261, align 8
  %263 = add i64 %262, %259
  store i64 %263, i64* %261, align 8
  %264 = load i64, i64* %40, align 8
  %265 = load i64, i64* %41, align 8
  %266 = mul i64 %264, %265
  %267 = trunc i64 %266 to i32
  store i32 %267, i32* %47, align 4
  %268 = load i32, i32* %47, align 4
  %269 = sext i32 %268 to i64
  %270 = icmp ne i64 %269, 8
  br i1 %270, label %271, label %274

; <label>:271:                                    ; preds = %242
  %272 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([41 x i8], [41 x i8]* @.str.1, i32 0, i32 0))
  %273 = sext i32 %272 to i64
  store i64 %273, i64* @order_gurantee3, align 8
  br label %497

; <label>:274:                                    ; preds = %242
  br label %275

; <label>:275:                                    ; preds = %462, %274
  %276 = load %struct.header_info*, %struct.header_info** %44, align 8
  %277 = bitcast %struct.TgHd* %46 to i8*
  %278 = load i8*, i8** %45, align 8
  store %struct.header_info* %276, %struct.header_info** %23, align 8
  store i8* %277, i8** %24, align 8
  store i64 1, i64* %25, align 8
  store i64 48, i64* %26, align 8
  store i8* %278, i8** %27, align 8
  %279 = load i8*, i8** %24, align 8
  %280 = load i8*, i8** %27, align 8
  %281 = load %struct.header_info*, %struct.header_info** %23, align 8
  %282 = getelementptr inbounds %struct.header_info, %struct.header_info* %281, i32 0, i32 1
  %283 = load i64, i64* %282, align 8
  %284 = getelementptr inbounds i8, i8* %280, i64 %283
  %285 = load i64, i64* %25, align 8
  %286 = load i64, i64* %26, align 8
  %287 = mul i64 %285, %286
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %279, i8* align 1 %284, i64 %287, i1 false) #7
  %288 = load i64, i64* %25, align 8
  %289 = load i64, i64* %26, align 8
  %290 = mul i64 %288, %289
  %291 = load %struct.header_info*, %struct.header_info** %23, align 8
  %292 = getelementptr inbounds %struct.header_info, %struct.header_info* %291, i32 0, i32 1
  %293 = load i64, i64* %292, align 8
  %294 = add i64 %293, %290
  store i64 %294, i64* %292, align 8
  %295 = load i64, i64* %25, align 8
  %296 = load i64, i64* %26, align 8
  %297 = mul i64 %295, %296
  %298 = trunc i64 %297 to i32
  store i32 %298, i32* %47, align 4
  %299 = load i32, i32* %47, align 4
  %300 = sext i32 %299 to i64
  %301 = icmp ne i64 %300, 48
  br i1 %301, label %302, label %303

; <label>:302:                                    ; preds = %275
  br label %497

; <label>:303:                                    ; preds = %275
  %304 = getelementptr inbounds [40 x i8], [40 x i8]* %51, i32 0, i32 0
  %305 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 0
  %306 = getelementptr inbounds [32 x i8], [32 x i8]* %305, i32 0, i32 0
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 16 %304, i8* align 8 %306, i64 40, i1 false)
  %307 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 1
  %308 = load i32, i32* %307, align 8
  %309 = icmp sgt i32 %308, -1
  br i1 %309, label %310, label %317

; <label>:310:                                    ; preds = %303
  %311 = getelementptr inbounds [40 x i8], [40 x i8]* %51, i32 0, i32 0
  %312 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 0
  %313 = getelementptr inbounds [32 x i8], [32 x i8]* %312, i32 0, i32 0
  %314 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 1
  %315 = load i32, i32* %314, align 8
  %316 = call i32 (i8*, i8*, ...) @sprintf(i8* %311, i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.2, i32 0, i32 0), i8* %313, i32 %315) #7
  br label %317

; <label>:317:                                    ; preds = %310, %303
  %318 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 2
  %319 = load i32, i32* %318, align 4
  switch i32 %319, label %461 [
    i32 -65528, label %320
    i32 8, label %321
    i32 268435464, label %322
    i32 285212680, label %333
    i32 301989896, label %334
    i32 536870920, label %335
    i32 537001983, label %364
    i32 553648136, label %369
    i32 1073872895, label %374
    i32 1073938431, label %412
    i32 -1, label %456
  ]

; <label>:320:                                    ; preds = %317
  br label %462

; <label>:321:                                    ; preds = %317
  br label %462

; <label>:322:                                    ; preds = %317
  %323 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 0
  %324 = getelementptr inbounds [32 x i8], [32 x i8]* %323, i32 0, i32 0
  %325 = call i32 @strcmp(i8* %324, i8* getelementptr inbounds ([27 x i8], [27 x i8]* @.str.3, i32 0, i32 0)) #8
  %326 = icmp eq i32 %325, 0
  br i1 %326, label %327, label %332

; <label>:327:                                    ; preds = %322
  %328 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %329 = load i64, i64* %328, align 8
  %330 = load %struct.header_info*, %struct.header_info** %44, align 8
  %331 = getelementptr inbounds %struct.header_info, %struct.header_info* %330, i32 0, i32 6
  store i64 %329, i64* %331, align 8
  br label %332

; <label>:332:                                    ; preds = %327, %322
  br label %462

; <label>:333:                                    ; preds = %317
  br label %462

; <label>:334:                                    ; preds = %317
  br label %462

; <label>:335:                                    ; preds = %317
  %336 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 0
  %337 = getelementptr inbounds [32 x i8], [32 x i8]* %336, i32 0, i32 0
  %338 = call i32 @strcmp(i8* %337, i8* getelementptr inbounds ([20 x i8], [20 x i8]* @.str.4, i32 0, i32 0)) #8
  %339 = icmp eq i32 %338, 0
  br i1 %339, label %340, label %349

; <label>:340:                                    ; preds = %335
  %341 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %342 = bitcast i64* %341 to double*
  %343 = load double, double* %342, align 8
  store double %343, double* %52, align 8
  %344 = load double, double* %52, align 8
  %345 = fmul double %344, 1.000000e+12
  %346 = fptosi double %345 to i64
  %347 = load %struct.header_info*, %struct.header_info** %44, align 8
  %348 = getelementptr inbounds %struct.header_info, %struct.header_info* %347, i32 0, i32 3
  store i64 %346, i64* %348, align 8
  br label %349

; <label>:349:                                    ; preds = %340, %335
  %350 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 0
  %351 = getelementptr inbounds [32 x i8], [32 x i8]* %350, i32 0, i32 0
  %352 = call i32 @strcmp(i8* %351, i8* getelementptr inbounds ([26 x i8], [26 x i8]* @.str.5, i32 0, i32 0)) #8
  %353 = icmp eq i32 %352, 0
  br i1 %353, label %354, label %363

; <label>:354:                                    ; preds = %349
  %355 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %356 = bitcast i64* %355 to double*
  %357 = load double, double* %356, align 8
  store double %357, double* %53, align 8
  %358 = load double, double* %53, align 8
  %359 = fmul double %358, 1.000000e+12
  %360 = fptosi double %359 to i64
  %361 = load %struct.header_info*, %struct.header_info** %44, align 8
  %362 = getelementptr inbounds %struct.header_info, %struct.header_info* %361, i32 0, i32 2
  store i64 %360, i64* %362, align 8
  br label %363

; <label>:363:                                    ; preds = %354, %349
  br label %462

; <label>:364:                                    ; preds = %317
  %365 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %366 = load i64, i64* %365, align 8
  %367 = load %struct.header_info*, %struct.header_info** %44, align 8
  %368 = getelementptr inbounds %struct.header_info, %struct.header_info* %367, i32 0, i32 1
  store i64 %366, i64* %368, align 8
  br label %462

; <label>:369:                                    ; preds = %317
  %370 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %371 = bitcast i64* %370 to double*
  %372 = load double, double* %371, align 8
  %373 = call i64 @_Z15TDateTime_TimeTd(double %372)
  store i64 %373, i64* %54, align 8
  br label %462

; <label>:374:                                    ; preds = %317
  %375 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %376 = load i64, i64* %375, align 8
  %377 = call noalias i8* @calloc(i64 %376, i64 1) #7
  store i8* %377, i8** %48, align 8
  %378 = load %struct.header_info*, %struct.header_info** %44, align 8
  %379 = load i8*, i8** %48, align 8
  %380 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %381 = load i64, i64* %380, align 8
  %382 = load i8*, i8** %45, align 8
  store %struct.header_info* %378, %struct.header_info** %28, align 8
  store i8* %379, i8** %29, align 8
  store i64 1, i64* %30, align 8
  store i64 %381, i64* %31, align 8
  store i8* %382, i8** %32, align 8
  %383 = load i8*, i8** %29, align 8
  %384 = load i8*, i8** %32, align 8
  %385 = load %struct.header_info*, %struct.header_info** %28, align 8
  %386 = getelementptr inbounds %struct.header_info, %struct.header_info* %385, i32 0, i32 1
  %387 = load i64, i64* %386, align 8
  %388 = getelementptr inbounds i8, i8* %384, i64 %387
  %389 = load i64, i64* %30, align 8
  %390 = load i64, i64* %31, align 8
  %391 = mul i64 %389, %390
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %383, i8* align 1 %388, i64 %391, i1 false) #7
  %392 = load i64, i64* %30, align 8
  %393 = load i64, i64* %31, align 8
  %394 = mul i64 %392, %393
  %395 = load %struct.header_info*, %struct.header_info** %28, align 8
  %396 = getelementptr inbounds %struct.header_info, %struct.header_info* %395, i32 0, i32 1
  %397 = load i64, i64* %396, align 8
  %398 = add i64 %397, %394
  store i64 %398, i64* %396, align 8
  %399 = load i64, i64* %30, align 8
  %400 = load i64, i64* %31, align 8
  %401 = mul i64 %399, %400
  %402 = trunc i64 %401 to i32
  store i32 %402, i32* %47, align 4
  %403 = load i32, i32* %47, align 4
  %404 = sext i32 %403 to i64
  %405 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %406 = load i64, i64* %405, align 8
  %407 = icmp ne i64 %404, %406
  br i1 %407, label %408, label %410

; <label>:408:                                    ; preds = %374
  %409 = load i8*, i8** %48, align 8
  call void @free(i8* %409) #7
  br label %497

; <label>:410:                                    ; preds = %374
  %411 = load i8*, i8** %48, align 8
  call void @free(i8* %411) #7
  br label %462

; <label>:412:                                    ; preds = %317
  %413 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %414 = load i64, i64* %413, align 8
  %415 = call noalias i8* @calloc(i64 %414, i64 1) #7
  %416 = bitcast i8* %415 to i32*
  store i32* %416, i32** %49, align 8
  %417 = load %struct.header_info*, %struct.header_info** %44, align 8
  %418 = load i32*, i32** %49, align 8
  %419 = bitcast i32* %418 to i8*
  %420 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %421 = load i64, i64* %420, align 8
  %422 = load i8*, i8** %45, align 8
  store %struct.header_info* %417, %struct.header_info** %33, align 8
  store i8* %419, i8** %34, align 8
  store i64 1, i64* %35, align 8
  store i64 %421, i64* %36, align 8
  store i8* %422, i8** %37, align 8
  %423 = load i8*, i8** %34, align 8
  %424 = load i8*, i8** %37, align 8
  %425 = load %struct.header_info*, %struct.header_info** %33, align 8
  %426 = getelementptr inbounds %struct.header_info, %struct.header_info* %425, i32 0, i32 1
  %427 = load i64, i64* %426, align 8
  %428 = getelementptr inbounds i8, i8* %424, i64 %427
  %429 = load i64, i64* %35, align 8
  %430 = load i64, i64* %36, align 8
  %431 = mul i64 %429, %430
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 1 %423, i8* align 1 %428, i64 %431, i1 false) #7
  %432 = load i64, i64* %35, align 8
  %433 = load i64, i64* %36, align 8
  %434 = mul i64 %432, %433
  %435 = load %struct.header_info*, %struct.header_info** %33, align 8
  %436 = getelementptr inbounds %struct.header_info, %struct.header_info* %435, i32 0, i32 1
  %437 = load i64, i64* %436, align 8
  %438 = add i64 %437, %434
  store i64 %438, i64* %436, align 8
  %439 = load i64, i64* %35, align 8
  %440 = load i64, i64* %36, align 8
  %441 = mul i64 %439, %440
  %442 = trunc i64 %441 to i32
  store i32 %442, i32* %47, align 4
  %443 = load i32, i32* %47, align 4
  %444 = sext i32 %443 to i64
  %445 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %446 = load i64, i64* %445, align 8
  %447 = icmp ne i64 %444, %446
  br i1 %447, label %448, label %451

; <label>:448:                                    ; preds = %412
  %449 = load i32*, i32** %49, align 8
  %450 = bitcast i32* %449 to i8*
  call void @free(i8* %450) #7
  br label %497

; <label>:451:                                    ; preds = %412
  %452 = load i32*, i32** %49, align 8
  %453 = call i32 (i32*, ...) @wprintf(i32* getelementptr inbounds ([3 x i32], [3 x i32]* @.str.6, i32 0, i32 0), i32* %452)
  %454 = load i32*, i32** %49, align 8
  %455 = bitcast i32* %454 to i8*
  call void @free(i8* %455) #7
  br label %462

; <label>:456:                                    ; preds = %317
  %457 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 3
  %458 = load i64, i64* %457, align 8
  %459 = load %struct.header_info*, %struct.header_info** %44, align 8
  %460 = getelementptr inbounds %struct.header_info, %struct.header_info* %459, i32 0, i32 1
  store i64 %458, i64* %460, align 8
  br label %462

; <label>:461:                                    ; preds = %317
  br label %497

; <label>:462:                                    ; preds = %456, %451, %410, %369, %364, %363, %334, %333, %332, %321, %320
  %463 = getelementptr inbounds %struct.TgHd, %struct.TgHd* %46, i32 0, i32 0
  %464 = getelementptr inbounds [32 x i8], [32 x i8]* %463, i32 0, i32 0
  %465 = call i32 @strncmp(i8* %464, i8* getelementptr inbounds ([11 x i8], [11 x i8]* @.str.7, i32 0, i32 0), i64 11) #8
  %466 = icmp ne i32 %465, 0
  br i1 %466, label %275, label %467

; <label>:467:                                    ; preds = %462
  %468 = load %struct.header_info*, %struct.header_info** %44, align 8
  %469 = getelementptr inbounds %struct.header_info, %struct.header_info* %468, i32 0, i32 6
  %470 = load i64, i64* %469, align 8
  switch i64 %470, label %481 [
    i64 66051, label %471
    i64 66052, label %472
    i64 16843268, label %473
    i64 66053, label %474
    i64 66054, label %475
    i64 66307, label %476
    i64 66308, label %477
    i64 16843524, label %478
    i64 66309, label %479
    i64 66310, label %480
  ]

; <label>:471:                                    ; preds = %467
  store i8 1, i8* %55, align 1
  br label %482

; <label>:472:                                    ; preds = %467
  store i8 1, i8* %55, align 1
  br label %482

; <label>:473:                                    ; preds = %467
  store i8 1, i8* %55, align 1
  br label %482

; <label>:474:                                    ; preds = %467
  store i8 1, i8* %55, align 1
  br label %482

; <label>:475:                                    ; preds = %467
  store i8 1, i8* %55, align 1
  br label %482

; <label>:476:                                    ; preds = %467
  store i8 0, i8* %55, align 1
  br label %482

; <label>:477:                                    ; preds = %467
  store i8 0, i8* %55, align 1
  br label %482

; <label>:478:                                    ; preds = %467
  store i8 0, i8* %55, align 1
  br label %482

; <label>:479:                                    ; preds = %467
  store i8 0, i8* %55, align 1
  br label %482

; <label>:480:                                    ; preds = %467
  store i8 0, i8* %55, align 1
  br label %482

; <label>:481:                                    ; preds = %467
  br label %497

; <label>:482:                                    ; preds = %480, %479, %478, %477, %476, %475, %474, %473, %472, %471
  %483 = load i8, i8* %55, align 1
  %484 = trunc i8 %483 to i1
  br i1 %484, label %485, label %488

; <label>:485:                                    ; preds = %482
  %486 = load %struct.header_info*, %struct.header_info** %44, align 8
  %487 = getelementptr inbounds %struct.header_info, %struct.header_info* %486, i32 0, i32 4
  store i64 1, i64* %487, align 8
  br label %494

; <label>:488:                                    ; preds = %482
  %489 = load %struct.header_info*, %struct.header_info** %44, align 8
  %490 = getelementptr inbounds %struct.header_info, %struct.header_info* %489, i32 0, i32 2
  %491 = load i64, i64* %490, align 8
  %492 = load %struct.header_info*, %struct.header_info** %44, align 8
  %493 = getelementptr inbounds %struct.header_info, %struct.header_info* %492, i32 0, i32 4
  store i64 %491, i64* %493, align 8
  br label %494

; <label>:494:                                    ; preds = %488, %485
  %495 = load %struct.header_info*, %struct.header_info** %44, align 8
  %496 = getelementptr inbounds %struct.header_info, %struct.header_info* %495, i32 0, i32 5
  store i64 4, i64* %496, align 8
  store i32 0, i32* %43, align 4
  br label %498

; <label>:497:                                    ; preds = %481, %461, %448, %408, %302, %271
  store i32 -1, i32* %43, align 4
  br label %498

; <label>:498:                                    ; preds = %494, %497
  %499 = load i32, i32* %43, align 4
  store i32 %499, i32* %64, align 4
  store i8 0, i8* %66, align 1
  br label %505

; <label>:500:                                    ; preds = %115
  %501 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([93 x i8], [93 x i8]* @.str.11, i32 0, i32 0))
  %502 = sext i32 %501 to i64
  store i64 %502, i64* @order_gurantee3, align 8
  store i32 -2, i32* %64, align 4
  %503 = load %struct.header_info*, %struct.header_info** %62, align 8
  %504 = getelementptr inbounds %struct.header_info, %struct.header_info* %503, i32 0, i32 5
  store i64 1, i64* %504, align 8
  br label %505

; <label>:505:                                    ; preds = %115, %500, %498, %223, %221, %164, %162
  %506 = load %struct.header_info*, %struct.header_info** %62, align 8
  %507 = getelementptr inbounds %struct.header_info, %struct.header_info* %506, i32 0, i32 1
  %508 = load i64, i64* %507, align 8
  %509 = load %struct.header_info*, %struct.header_info** %62, align 8
  %510 = getelementptr inbounds %struct.header_info, %struct.header_info* %509, i32 0, i32 0
  store i64 %508, i64* %510, align 8
  %511 = load i32, i32* %64, align 4
  store i32 %511, i32* %61, align 4
  br label %512

; <label>:512:                                    ; preds = %505, %92
  %513 = load i32, i32* %61, align 4
  ret i32 %513
}

attributes #0 = { alwaysinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { argmemonly nounwind }
attributes #2 = { alwaysinline uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #5 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #6 = { nounwind readonly "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #7 = { nounwind }
attributes #8 = { nounwind readonly }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 8.0.1-9 (tags/RELEASE_801/final)"}
