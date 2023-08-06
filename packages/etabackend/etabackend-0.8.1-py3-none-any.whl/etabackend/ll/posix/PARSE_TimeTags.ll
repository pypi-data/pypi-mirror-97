; ModuleID = 'etabackend/cpp/PARSE_TimeTags.cpp'
source_filename = "etabackend/cpp/PARSE_TimeTags.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

%struct.ttf_reader = type { i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i64, i8* }
%union.anon = type { i32 }
%struct.anon = type { i32 }
%union.anon.0 = type { i64 }
%struct.anon.1 = type { i32 }
%union.anon.2 = type { i32 }
%struct.anon.3 = type { i32 }
%struct.anon.4 = type { i32 }
%union.anon.5 = type { i32 }
%struct.anon.6 = type { i32 }
%struct.TTTRRecord = type { i64, i16 }
%struct.SITTTRStruct = type { i32, i32, i64 }
%union.COMPTTTRRecord = type { %struct.anon.7 }
%struct.anon.7 = type { i40 }
%union.bh4bytesRec = type { i32 }
%struct.anon.8 = type { i32 }

@order_gurantee = dso_local global i64 0, align 8
@.str = private unnamed_addr constant [30 x i8] c"\0A [FATAL] Illegal Chan:  %1u\0A\00", align 1
@.str.1 = private unnamed_addr constant [40 x i8] c"\0A [FATAL]\0AIllegal virtual_channel:  %1u\00", align 1
@.str.2 = private unnamed_addr constant [44 x i8] c"\0A [ERROR]ERROR: Unsupported timetag format.\00", align 1

; Function Attrs: alwaysinline uwtable
define dso_local void @ProcessPHT2(%struct.ttf_reader*, i32, i64* dereferenceable(8), i8* dereferenceable(1), i64* dereferenceable(8)) #0 {
  %6 = alloca %struct.ttf_reader*, align 8
  %7 = alloca i32, align 4
  %8 = alloca i64*, align 8
  %9 = alloca i8*, align 8
  %10 = alloca i64*, align 8
  %11 = alloca i32, align 4
  %12 = alloca i64, align 8
  %13 = alloca %union.anon, align 4
  %14 = alloca i32, align 4
  store %struct.ttf_reader* %0, %struct.ttf_reader** %6, align 8
  store i32 %1, i32* %7, align 4
  store i64* %2, i64** %8, align 8
  store i8* %3, i8** %9, align 8
  store i64* %4, i64** %10, align 8
  store i32 210698240, i32* %11, align 4
  %15 = load i32, i32* %7, align 4
  %16 = bitcast %union.anon* %13 to i32*
  store i32 %15, i32* %16, align 4
  %17 = bitcast %union.anon* %13 to %struct.anon*
  %18 = bitcast %struct.anon* %17 to i32*
  %19 = load i32, i32* %18, align 4
  %20 = lshr i32 %19, 28
  %21 = icmp eq i32 %20, 15
  br i1 %21, label %22, label %59

; <label>:22:                                     ; preds = %5
  %23 = bitcast %union.anon* %13 to %struct.anon*
  %24 = bitcast %struct.anon* %23 to i32*
  %25 = load i32, i32* %24, align 4
  %26 = and i32 %25, 268435455
  %27 = and i32 %26, 15
  store i32 %27, i32* %14, align 4
  %28 = load i32, i32* %14, align 4
  %29 = icmp eq i32 %28, 0
  br i1 %29, label %30, label %34

; <label>:30:                                     ; preds = %22
  %31 = load i64*, i64** %10, align 8
  %32 = load i64, i64* %31, align 8
  %33 = add nsw i64 %32, 210698240
  store i64 %33, i64* %31, align 8
  br label %58

; <label>:34:                                     ; preds = %22
  %35 = load i64*, i64** %10, align 8
  %36 = load i64, i64* %35, align 8
  %37 = bitcast %union.anon* %13 to %struct.anon*
  %38 = bitcast %struct.anon* %37 to i32*
  %39 = load i32, i32* %38, align 4
  %40 = and i32 %39, 268435455
  %41 = zext i32 %40 to i64
  %42 = add nsw i64 %36, %41
  store i64 %42, i64* %12, align 8
  %43 = load i64, i64* %12, align 8
  %44 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %45 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %44, i32 0, i32 2
  %46 = load i64, i64* %45, align 8
  %47 = mul nsw i64 %43, %46
  %48 = load i64*, i64** %8, align 8
  store i64 %47, i64* %48, align 8
  %49 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %50 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %49, i32 0, i32 9
  %51 = load i64, i64* %50, align 8
  %52 = load i32, i32* %14, align 4
  %53 = call i32 @llvm.cttz.i32(i32 %52, i1 true)
  %54 = sext i32 %53 to i64
  %55 = add nsw i64 %51, %54
  %56 = trunc i64 %55 to i8
  %57 = load i8*, i8** %9, align 8
  store i8 %56, i8* %57, align 1
  br label %58

; <label>:58:                                     ; preds = %34, %30
  br label %102

; <label>:59:                                     ; preds = %5
  %60 = bitcast %union.anon* %13 to %struct.anon*
  %61 = bitcast %struct.anon* %60 to i32*
  %62 = load i32, i32* %61, align 4
  %63 = lshr i32 %62, 28
  %64 = icmp sgt i32 %63, 4
  br i1 %64, label %65, label %75

; <label>:65:                                     ; preds = %59
  %66 = bitcast %union.anon* %13 to %struct.anon*
  %67 = bitcast %struct.anon* %66 to i32*
  %68 = load i32, i32* %67, align 4
  %69 = lshr i32 %68, 28
  %70 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.str, i32 0, i32 0), i32 %69)
  %71 = sext i32 %70 to i64
  store i64 %71, i64* @order_gurantee, align 8
  br label %72

; <label>:72:                                     ; preds = %65, %72
  %73 = load i64, i64* @order_gurantee, align 8
  %74 = add nsw i64 %73, 1
  store i64 %74, i64* @order_gurantee, align 8
  br label %72

; <label>:75:                                     ; preds = %59
  %76 = load i64*, i64** %10, align 8
  %77 = load i64, i64* %76, align 8
  %78 = bitcast %union.anon* %13 to %struct.anon*
  %79 = bitcast %struct.anon* %78 to i32*
  %80 = load i32, i32* %79, align 4
  %81 = and i32 %80, 268435455
  %82 = zext i32 %81 to i64
  %83 = add nsw i64 %77, %82
  store i64 %83, i64* %12, align 8
  %84 = load i64, i64* %12, align 8
  %85 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %86 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %85, i32 0, i32 2
  %87 = load i64, i64* %86, align 8
  %88 = mul nsw i64 %84, %87
  %89 = load i64*, i64** %8, align 8
  store i64 %88, i64* %89, align 8
  %90 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %91 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %90, i32 0, i32 8
  %92 = load i64, i64* %91, align 8
  %93 = bitcast %union.anon* %13 to %struct.anon*
  %94 = bitcast %struct.anon* %93 to i32*
  %95 = load i32, i32* %94, align 4
  %96 = lshr i32 %95, 28
  %97 = zext i32 %96 to i64
  %98 = add nsw i64 %92, %97
  %99 = trunc i64 %98 to i8
  %100 = load i8*, i8** %9, align 8
  store i8 %99, i8* %100, align 1
  br label %101

; <label>:101:                                    ; preds = %75
  br label %102

; <label>:102:                                    ; preds = %101, %58
  ret void
}

; Function Attrs: nounwind readnone speculatable
declare i32 @llvm.cttz.i32(i32, i1) #1

declare dso_local i32 @printf(i8*, ...) #2

; Function Attrs: alwaysinline nounwind uwtable
define dso_local void @ProcessHHT2(%struct.ttf_reader*, i32, i32, i64* dereferenceable(8), i8* dereferenceable(1), i64* dereferenceable(8)) #3 {
  %7 = alloca %struct.ttf_reader*, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i64*, align 8
  %11 = alloca i8*, align 8
  %12 = alloca i64*, align 8
  %13 = alloca i64, align 8
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca %union.anon.0, align 8
  store %struct.ttf_reader* %0, %struct.ttf_reader** %7, align 8
  store i32 %1, i32* %8, align 4
  store i32 %2, i32* %9, align 4
  store i64* %3, i64** %10, align 8
  store i8* %4, i8** %11, align 8
  store i64* %5, i64** %12, align 8
  store i32 33552000, i32* %14, align 4
  store i32 33554432, i32* %15, align 4
  %17 = load i32, i32* %8, align 4
  %18 = zext i32 %17 to i64
  %19 = bitcast %union.anon.0* %16 to i64*
  store i64 %18, i64* %19, align 8
  %20 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %21 = bitcast %struct.anon.1* %20 to i32*
  %22 = load i32, i32* %21, align 8
  %23 = lshr i32 %22, 31
  %24 = icmp eq i32 %23, 1
  br i1 %24, label %25, label %132

; <label>:25:                                     ; preds = %6
  %26 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %27 = bitcast %struct.anon.1* %26 to i32*
  %28 = load i32, i32* %27, align 8
  %29 = lshr i32 %28, 25
  %30 = and i32 %29, 63
  %31 = icmp eq i32 %30, 63
  br i1 %31, label %32, label %61

; <label>:32:                                     ; preds = %25
  %33 = load i32, i32* %9, align 4
  %34 = icmp eq i32 %33, 1
  br i1 %34, label %35, label %39

; <label>:35:                                     ; preds = %32
  %36 = load i64*, i64** %12, align 8
  %37 = load i64, i64* %36, align 8
  %38 = add i64 %37, 33552000
  store i64 %38, i64* %36, align 8
  br label %60

; <label>:39:                                     ; preds = %32
  %40 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %41 = bitcast %struct.anon.1* %40 to i32*
  %42 = load i32, i32* %41, align 8
  %43 = and i32 %42, 33554431
  %44 = icmp eq i32 %43, 0
  br i1 %44, label %45, label %49

; <label>:45:                                     ; preds = %39
  %46 = load i64*, i64** %12, align 8
  %47 = load i64, i64* %46, align 8
  %48 = add i64 %47, 33554432
  store i64 %48, i64* %46, align 8
  br label %59

; <label>:49:                                     ; preds = %39
  %50 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %51 = bitcast %struct.anon.1* %50 to i32*
  %52 = load i32, i32* %51, align 8
  %53 = and i32 %52, 33554431
  %54 = zext i32 %53 to i64
  %55 = mul i64 33554432, %54
  %56 = load i64*, i64** %12, align 8
  %57 = load i64, i64* %56, align 8
  %58 = add i64 %57, %55
  store i64 %58, i64* %56, align 8
  br label %59

; <label>:59:                                     ; preds = %49, %45
  br label %60

; <label>:60:                                     ; preds = %59, %35
  br label %61

; <label>:61:                                     ; preds = %60, %25
  %62 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %63 = bitcast %struct.anon.1* %62 to i32*
  %64 = load i32, i32* %63, align 8
  %65 = lshr i32 %64, 25
  %66 = and i32 %65, 63
  %67 = icmp sge i32 %66, 1
  br i1 %67, label %68, label %103

; <label>:68:                                     ; preds = %61
  %69 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %70 = bitcast %struct.anon.1* %69 to i32*
  %71 = load i32, i32* %70, align 8
  %72 = lshr i32 %71, 25
  %73 = and i32 %72, 63
  %74 = icmp sle i32 %73, 15
  br i1 %74, label %75, label %103

; <label>:75:                                     ; preds = %68
  %76 = load i64*, i64** %12, align 8
  %77 = load i64, i64* %76, align 8
  %78 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %79 = bitcast %struct.anon.1* %78 to i32*
  %80 = load i32, i32* %79, align 8
  %81 = and i32 %80, 33554431
  %82 = zext i32 %81 to i64
  %83 = add nsw i64 %77, %82
  store i64 %83, i64* %13, align 8
  %84 = load i64, i64* %13, align 8
  %85 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %86 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %85, i32 0, i32 2
  %87 = load i64, i64* %86, align 8
  %88 = mul nsw i64 %84, %87
  %89 = load i64*, i64** %10, align 8
  store i64 %88, i64* %89, align 8
  %90 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %91 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %90, i32 0, i32 9
  %92 = load i64, i64* %91, align 8
  %93 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %94 = bitcast %struct.anon.1* %93 to i32*
  %95 = load i32, i32* %94, align 8
  %96 = lshr i32 %95, 25
  %97 = and i32 %96, 63
  %98 = call i32 @llvm.cttz.i32(i32 %97, i1 true)
  %99 = sext i32 %98 to i64
  %100 = add nsw i64 %92, %99
  %101 = trunc i64 %100 to i8
  %102 = load i8*, i8** %11, align 8
  store i8 %101, i8* %102, align 1
  br label %103

; <label>:103:                                    ; preds = %75, %68, %61
  %104 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %105 = bitcast %struct.anon.1* %104 to i32*
  %106 = load i32, i32* %105, align 8
  %107 = lshr i32 %106, 25
  %108 = and i32 %107, 63
  %109 = icmp eq i32 %108, 0
  br i1 %109, label %110, label %131

; <label>:110:                                    ; preds = %103
  %111 = load i64*, i64** %12, align 8
  %112 = load i64, i64* %111, align 8
  %113 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %114 = bitcast %struct.anon.1* %113 to i32*
  %115 = load i32, i32* %114, align 8
  %116 = and i32 %115, 33554431
  %117 = zext i32 %116 to i64
  %118 = add nsw i64 %112, %117
  store i64 %118, i64* %13, align 8
  %119 = load i64, i64* %13, align 8
  %120 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %121 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %120, i32 0, i32 2
  %122 = load i64, i64* %121, align 8
  %123 = mul nsw i64 %119, %122
  %124 = load i64*, i64** %10, align 8
  store i64 %123, i64* %124, align 8
  %125 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %126 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %125, i32 0, i32 8
  %127 = load i64, i64* %126, align 8
  %128 = add nsw i64 %127, 0
  %129 = trunc i64 %128 to i8
  %130 = load i8*, i8** %11, align 8
  store i8 %129, i8* %130, align 1
  br label %131

; <label>:131:                                    ; preds = %110, %103
  br label %160

; <label>:132:                                    ; preds = %6
  %133 = load i64*, i64** %12, align 8
  %134 = load i64, i64* %133, align 8
  %135 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %136 = bitcast %struct.anon.1* %135 to i32*
  %137 = load i32, i32* %136, align 8
  %138 = and i32 %137, 33554431
  %139 = zext i32 %138 to i64
  %140 = add nsw i64 %134, %139
  store i64 %140, i64* %13, align 8
  %141 = load i64, i64* %13, align 8
  %142 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %143 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %142, i32 0, i32 2
  %144 = load i64, i64* %143, align 8
  %145 = mul nsw i64 %141, %144
  %146 = load i64*, i64** %10, align 8
  store i64 %145, i64* %146, align 8
  %147 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %148 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %147, i32 0, i32 8
  %149 = load i64, i64* %148, align 8
  %150 = bitcast %union.anon.0* %16 to %struct.anon.1*
  %151 = bitcast %struct.anon.1* %150 to i32*
  %152 = load i32, i32* %151, align 8
  %153 = lshr i32 %152, 25
  %154 = and i32 %153, 63
  %155 = zext i32 %154 to i64
  %156 = add nsw i64 %149, %155
  %157 = add nsw i64 %156, 1
  %158 = trunc i64 %157 to i8
  %159 = load i8*, i8** %11, align 8
  store i8 %158, i8* %159, align 1
  br label %160

; <label>:160:                                    ; preds = %132, %131
  ret void
}

; Function Attrs: alwaysinline uwtable
define dso_local void @ProcessPHT3(%struct.ttf_reader*, i32, i64* dereferenceable(8), i8* dereferenceable(1), i64* dereferenceable(8)) #0 {
  %6 = alloca %struct.ttf_reader*, align 8
  %7 = alloca i32, align 4
  %8 = alloca i64*, align 8
  %9 = alloca i8*, align 8
  %10 = alloca i64*, align 8
  %11 = alloca i64, align 8
  %12 = alloca i32, align 4
  %13 = alloca %union.anon.2, align 4
  store %struct.ttf_reader* %0, %struct.ttf_reader** %6, align 8
  store i32 %1, i32* %7, align 4
  store i64* %2, i64** %8, align 8
  store i8* %3, i8** %9, align 8
  store i64* %4, i64** %10, align 8
  store i32 65536, i32* %12, align 4
  %14 = load i32, i32* %7, align 4
  %15 = bitcast %union.anon.2* %13 to i32*
  store i32 %14, i32* %15, align 4
  %16 = bitcast %union.anon.2* %13 to %struct.anon.3*
  %17 = bitcast %struct.anon.3* %16 to i32*
  %18 = load i32, i32* %17, align 4
  %19 = lshr i32 %18, 28
  %20 = icmp eq i32 %19, 15
  br i1 %20, label %21, label %66

; <label>:21:                                     ; preds = %5
  %22 = bitcast %union.anon.2* %13 to %struct.anon.4*
  %23 = bitcast %struct.anon.4* %22 to i32*
  %24 = load i32, i32* %23, align 4
  %25 = lshr i32 %24, 16
  %26 = and i32 %25, 4095
  %27 = icmp eq i32 %26, 0
  br i1 %27, label %28, label %32

; <label>:28:                                     ; preds = %21
  %29 = load i64*, i64** %10, align 8
  %30 = load i64, i64* %29, align 8
  %31 = add nsw i64 %30, 65536
  store i64 %31, i64* %29, align 8
  br label %65

; <label>:32:                                     ; preds = %21
  %33 = load i64*, i64** %10, align 8
  %34 = load i64, i64* %33, align 8
  %35 = bitcast %union.anon.2* %13 to %struct.anon.3*
  %36 = bitcast %struct.anon.3* %35 to i32*
  %37 = load i32, i32* %36, align 4
  %38 = and i32 %37, 65535
  %39 = zext i32 %38 to i64
  %40 = add nsw i64 %34, %39
  store i64 %40, i64* %11, align 8
  %41 = load i64, i64* %11, align 8
  %42 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %43 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %42, i32 0, i32 4
  %44 = load i64, i64* %43, align 8
  %45 = mul nsw i64 %41, %44
  %46 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %47 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %46, i32 0, i32 3
  %48 = load i64, i64* %47, align 8
  %49 = mul nsw i64 0, %48
  %50 = add nsw i64 %45, %49
  %51 = load i64*, i64** %8, align 8
  store i64 %50, i64* %51, align 8
  %52 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %53 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %52, i32 0, i32 9
  %54 = load i64, i64* %53, align 8
  %55 = bitcast %union.anon.2* %13 to %struct.anon.4*
  %56 = bitcast %struct.anon.4* %55 to i32*
  %57 = load i32, i32* %56, align 4
  %58 = lshr i32 %57, 16
  %59 = and i32 %58, 4095
  %60 = call i32 @llvm.cttz.i32(i32 %59, i1 true)
  %61 = sext i32 %60 to i64
  %62 = add nsw i64 %54, %61
  %63 = trunc i64 %62 to i8
  %64 = load i8*, i8** %9, align 8
  store i8 %63, i8* %64, align 1
  br label %65

; <label>:65:                                     ; preds = %32, %28
  br label %125

; <label>:66:                                     ; preds = %5
  %67 = bitcast %union.anon.2* %13 to %struct.anon.3*
  %68 = bitcast %struct.anon.3* %67 to i32*
  %69 = load i32, i32* %68, align 4
  %70 = lshr i32 %69, 28
  %71 = icmp eq i32 %70, 0
  br i1 %71, label %78, label %72

; <label>:72:                                     ; preds = %66
  %73 = bitcast %union.anon.2* %13 to %struct.anon.3*
  %74 = bitcast %struct.anon.3* %73 to i32*
  %75 = load i32, i32* %74, align 4
  %76 = lshr i32 %75, 28
  %77 = icmp sgt i32 %76, 4
  br i1 %77, label %78, label %88

; <label>:78:                                     ; preds = %72, %66
  %79 = bitcast %union.anon.2* %13 to %struct.anon.3*
  %80 = bitcast %struct.anon.3* %79 to i32*
  %81 = load i32, i32* %80, align 4
  %82 = lshr i32 %81, 28
  %83 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([40 x i8], [40 x i8]* @.str.1, i32 0, i32 0), i32 %82)
  %84 = sext i32 %83 to i64
  store i64 %84, i64* @order_gurantee, align 8
  br label %85

; <label>:85:                                     ; preds = %78, %85
  %86 = load i64, i64* @order_gurantee, align 8
  %87 = add nsw i64 %86, 1
  store i64 %87, i64* @order_gurantee, align 8
  br label %85

; <label>:88:                                     ; preds = %72
  %89 = load i64*, i64** %10, align 8
  %90 = load i64, i64* %89, align 8
  %91 = bitcast %union.anon.2* %13 to %struct.anon.3*
  %92 = bitcast %struct.anon.3* %91 to i32*
  %93 = load i32, i32* %92, align 4
  %94 = and i32 %93, 65535
  %95 = zext i32 %94 to i64
  %96 = add nsw i64 %90, %95
  store i64 %96, i64* %11, align 8
  %97 = load i64, i64* %11, align 8
  %98 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %99 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %98, i32 0, i32 4
  %100 = load i64, i64* %99, align 8
  %101 = mul nsw i64 %97, %100
  %102 = bitcast %union.anon.2* %13 to %struct.anon.3*
  %103 = bitcast %struct.anon.3* %102 to i32*
  %104 = load i32, i32* %103, align 4
  %105 = lshr i32 %104, 16
  %106 = and i32 %105, 4095
  %107 = zext i32 %106 to i64
  %108 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %109 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %108, i32 0, i32 3
  %110 = load i64, i64* %109, align 8
  %111 = mul nsw i64 %107, %110
  %112 = add nsw i64 %101, %111
  %113 = load i64*, i64** %8, align 8
  store i64 %112, i64* %113, align 8
  %114 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %115 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %114, i32 0, i32 8
  %116 = load i64, i64* %115, align 8
  %117 = bitcast %union.anon.2* %13 to %struct.anon.3*
  %118 = bitcast %struct.anon.3* %117 to i32*
  %119 = load i32, i32* %118, align 4
  %120 = lshr i32 %119, 28
  %121 = zext i32 %120 to i64
  %122 = add nsw i64 %116, %121
  %123 = trunc i64 %122 to i8
  %124 = load i8*, i8** %9, align 8
  store i8 %123, i8* %124, align 1
  br label %125

; <label>:125:                                    ; preds = %88, %65
  ret void
}

; Function Attrs: alwaysinline nounwind uwtable
define dso_local void @ProcessHHT3(%struct.ttf_reader*, i32, i32, i64* dereferenceable(8), i8* dereferenceable(1), i64* dereferenceable(8)) #3 {
  %7 = alloca %struct.ttf_reader*, align 8
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca i64*, align 8
  %11 = alloca i8*, align 8
  %12 = alloca i64*, align 8
  %13 = alloca i32, align 4
  %14 = alloca %union.anon.5, align 4
  store %struct.ttf_reader* %0, %struct.ttf_reader** %7, align 8
  store i32 %1, i32* %8, align 4
  store i32 %2, i32* %9, align 4
  store i64* %3, i64** %10, align 8
  store i8* %4, i8** %11, align 8
  store i64* %5, i64** %12, align 8
  store i32 1024, i32* %13, align 4
  %15 = load i32, i32* %8, align 4
  %16 = bitcast %union.anon.5* %14 to i32*
  store i32 %15, i32* %16, align 4
  %17 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %18 = bitcast %struct.anon.6* %17 to i32*
  %19 = load i32, i32* %18, align 4
  %20 = lshr i32 %19, 31
  %21 = icmp eq i32 %20, 1
  br i1 %21, label %22, label %100

; <label>:22:                                     ; preds = %6
  %23 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %24 = bitcast %struct.anon.6* %23 to i32*
  %25 = load i32, i32* %24, align 4
  %26 = lshr i32 %25, 25
  %27 = and i32 %26, 63
  %28 = icmp eq i32 %27, 63
  br i1 %28, label %29, label %53

; <label>:29:                                     ; preds = %22
  %30 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %31 = bitcast %struct.anon.6* %30 to i32*
  %32 = load i32, i32* %31, align 4
  %33 = and i32 %32, 1023
  %34 = icmp eq i32 %33, 0
  br i1 %34, label %38, label %35

; <label>:35:                                     ; preds = %29
  %36 = load i32, i32* %9, align 4
  %37 = icmp eq i32 %36, 1
  br i1 %37, label %38, label %42

; <label>:38:                                     ; preds = %35, %29
  %39 = load i64*, i64** %12, align 8
  %40 = load i64, i64* %39, align 8
  %41 = add i64 %40, 1024
  store i64 %41, i64* %39, align 8
  br label %52

; <label>:42:                                     ; preds = %35
  %43 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %44 = bitcast %struct.anon.6* %43 to i32*
  %45 = load i32, i32* %44, align 4
  %46 = and i32 %45, 1023
  %47 = zext i32 %46 to i64
  %48 = mul i64 1024, %47
  %49 = load i64*, i64** %12, align 8
  %50 = load i64, i64* %49, align 8
  %51 = add i64 %50, %48
  store i64 %51, i64* %49, align 8
  br label %52

; <label>:52:                                     ; preds = %42, %38
  br label %53

; <label>:53:                                     ; preds = %52, %22
  %54 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %55 = bitcast %struct.anon.6* %54 to i32*
  %56 = load i32, i32* %55, align 4
  %57 = lshr i32 %56, 25
  %58 = and i32 %57, 63
  %59 = icmp sge i32 %58, 1
  br i1 %59, label %60, label %99

; <label>:60:                                     ; preds = %53
  %61 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %62 = bitcast %struct.anon.6* %61 to i32*
  %63 = load i32, i32* %62, align 4
  %64 = lshr i32 %63, 25
  %65 = and i32 %64, 63
  %66 = icmp sle i32 %65, 15
  br i1 %66, label %67, label %99

; <label>:67:                                     ; preds = %60
  %68 = load i64*, i64** %12, align 8
  %69 = load i64, i64* %68, align 8
  %70 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %71 = bitcast %struct.anon.6* %70 to i32*
  %72 = load i32, i32* %71, align 4
  %73 = and i32 %72, 1023
  %74 = zext i32 %73 to i64
  %75 = add nsw i64 %69, %74
  %76 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %77 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %76, i32 0, i32 4
  %78 = load i64, i64* %77, align 8
  %79 = mul nsw i64 %75, %78
  %80 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %81 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %80, i32 0, i32 3
  %82 = load i64, i64* %81, align 8
  %83 = mul nsw i64 0, %82
  %84 = add nsw i64 %79, %83
  %85 = load i64*, i64** %10, align 8
  store i64 %84, i64* %85, align 8
  %86 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %87 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %86, i32 0, i32 9
  %88 = load i64, i64* %87, align 8
  %89 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %90 = bitcast %struct.anon.6* %89 to i32*
  %91 = load i32, i32* %90, align 4
  %92 = lshr i32 %91, 25
  %93 = and i32 %92, 63
  %94 = call i32 @llvm.cttz.i32(i32 %93, i1 true)
  %95 = sext i32 %94 to i64
  %96 = add nsw i64 %88, %95
  %97 = trunc i64 %96 to i8
  %98 = load i8*, i8** %11, align 8
  store i8 %97, i8* %98, align 1
  br label %99

; <label>:99:                                     ; preds = %67, %60, %53
  br label %137

; <label>:100:                                    ; preds = %6
  %101 = load i64*, i64** %12, align 8
  %102 = load i64, i64* %101, align 8
  %103 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %104 = bitcast %struct.anon.6* %103 to i32*
  %105 = load i32, i32* %104, align 4
  %106 = and i32 %105, 1023
  %107 = zext i32 %106 to i64
  %108 = add nsw i64 %102, %107
  %109 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %110 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %109, i32 0, i32 4
  %111 = load i64, i64* %110, align 8
  %112 = mul nsw i64 %108, %111
  %113 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %114 = bitcast %struct.anon.6* %113 to i32*
  %115 = load i32, i32* %114, align 4
  %116 = lshr i32 %115, 10
  %117 = and i32 %116, 32767
  %118 = zext i32 %117 to i64
  %119 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %120 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %119, i32 0, i32 3
  %121 = load i64, i64* %120, align 8
  %122 = mul nsw i64 %118, %121
  %123 = add nsw i64 %112, %122
  %124 = load i64*, i64** %10, align 8
  store i64 %123, i64* %124, align 8
  %125 = load %struct.ttf_reader*, %struct.ttf_reader** %7, align 8
  %126 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %125, i32 0, i32 8
  %127 = load i64, i64* %126, align 8
  %128 = bitcast %union.anon.5* %14 to %struct.anon.6*
  %129 = bitcast %struct.anon.6* %128 to i32*
  %130 = load i32, i32* %129, align 4
  %131 = lshr i32 %130, 25
  %132 = and i32 %131, 63
  %133 = zext i32 %132 to i64
  %134 = add nsw i64 %127, %133
  %135 = trunc i64 %134 to i8
  %136 = load i8*, i8** %11, align 8
  store i8 %135, i8* %136, align 1
  br label %137

; <label>:137:                                    ; preds = %100, %99
  ret void
}

; Function Attrs: alwaysinline uwtable
define dso_local i64 @FileReader_pop_event(%struct.ttf_reader*, i8 zeroext, i8*) #0 {
  %4 = alloca %struct.ttf_reader*, align 8
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i64*, align 8
  %8 = alloca i8*, align 8
  %9 = alloca i64*, align 8
  %10 = alloca i32, align 4
  %11 = alloca %union.anon.5, align 4
  %12 = alloca %struct.ttf_reader*, align 8
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i64*, align 8
  %16 = alloca i8*, align 8
  %17 = alloca i64*, align 8
  %18 = alloca i64, align 8
  %19 = alloca i32, align 4
  %20 = alloca i32, align 4
  %21 = alloca %union.anon.0, align 8
  %22 = alloca %struct.ttf_reader*, align 8
  %23 = alloca i32, align 4
  %24 = alloca i32, align 4
  %25 = alloca i64*, align 8
  %26 = alloca i8*, align 8
  %27 = alloca i64*, align 8
  %28 = alloca i32, align 4
  %29 = alloca %union.anon.5, align 4
  %30 = alloca %struct.ttf_reader*, align 8
  %31 = alloca i32, align 4
  %32 = alloca i32, align 4
  %33 = alloca i64*, align 8
  %34 = alloca i8*, align 8
  %35 = alloca i64*, align 8
  %36 = alloca i64, align 8
  %37 = alloca i32, align 4
  %38 = alloca i32, align 4
  %39 = alloca %union.anon.0, align 8
  %40 = alloca %struct.ttf_reader*, align 8
  %41 = alloca i32, align 4
  %42 = alloca i64*, align 8
  %43 = alloca i8*, align 8
  %44 = alloca i64*, align 8
  %45 = alloca i64, align 8
  %46 = alloca i32, align 4
  %47 = alloca %union.anon.2, align 4
  %48 = alloca %struct.ttf_reader*, align 8
  %49 = alloca i32, align 4
  %50 = alloca i64*, align 8
  %51 = alloca i8*, align 8
  %52 = alloca i64*, align 8
  %53 = alloca i32, align 4
  %54 = alloca i64, align 8
  %55 = alloca %union.anon, align 4
  %56 = alloca i32, align 4
  %57 = alloca i64, align 8
  %58 = alloca %struct.ttf_reader*, align 8
  %59 = alloca i8, align 1
  %60 = alloca i8*, align 8
  %61 = alloca %struct.ttf_reader*, align 8
  %62 = alloca i64, align 8
  %63 = alloca i8, align 1
  %64 = alloca i64, align 8
  %65 = alloca i64, align 8
  %66 = alloca i64, align 8
  %67 = alloca i32, align 4
  %68 = alloca %struct.TTTRRecord, align 8
  %69 = alloca %struct.TTTRRecord*, align 8
  %70 = alloca %struct.SITTTRStruct*, align 8
  %71 = alloca %union.COMPTTTRRecord*, align 8
  %72 = alloca %union.bh4bytesRec*, align 8
  store %struct.ttf_reader* %0, %struct.ttf_reader** %58, align 8
  store i8 %1, i8* %59, align 1
  store i8* %2, i8** %60, align 8
  %73 = load %struct.ttf_reader*, %struct.ttf_reader** %58, align 8
  %74 = load i8, i8* %59, align 1
  %75 = zext i8 %74 to i64
  %76 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %73, i64 %75
  store %struct.ttf_reader* %76, %struct.ttf_reader** %61, align 8
  br label %77

; <label>:77:                                     ; preds = %3, %1068
  store i64 9223372036854775807, i64* %62, align 8
  store i8 -1, i8* %63, align 1
  %78 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %79 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %78, i32 0, i32 11
  %80 = load i64, i64* %79, align 8
  %81 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %82 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %81, i32 0, i32 5
  %83 = load i64, i64* %82, align 8
  %84 = mul nsw i64 %80, %83
  store i64 %84, i64* %64, align 8
  %85 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %86 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %85, i32 0, i32 0
  %87 = load i64, i64* %86, align 8
  %88 = load i64, i64* %64, align 8
  %89 = add nsw i64 %87, %88
  store i64 %89, i64* %65, align 8
  %90 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %91 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %90, i32 0, i32 0
  %92 = load i64, i64* %91, align 8
  %93 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %94 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %93, i32 0, i32 10
  %95 = load i64, i64* %94, align 8
  %96 = add nsw i64 %92, %95
  store i64 %96, i64* %66, align 8
  %97 = load i64, i64* %64, align 8
  %98 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %99 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %98, i32 0, i32 10
  %100 = load i64, i64* %99, align 8
  %101 = icmp sge i64 %97, %100
  br i1 %101, label %102, label %103

; <label>:102:                                    ; preds = %77
  br label %1077

; <label>:103:                                    ; preds = %77
  %104 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %105 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %104, i32 0, i32 14
  %106 = load i8*, i8** %105, align 8
  %107 = bitcast i8* %106 to i32*
  %108 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %109 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %108, i32 0, i32 11
  %110 = load i64, i64* %109, align 8
  %111 = getelementptr inbounds i32, i32* %107, i64 %110
  %112 = load i32, i32* %111, align 4
  store i32 %112, i32* %67, align 4
  %113 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %114 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %113, i32 0, i32 6
  %115 = load i64, i64* %114, align 8
  switch i64 %115, label %1058 [
    i64 66051, label %116
    i64 66307, label %208
    i64 66052, label %323
    i64 66308, label %471
    i64 16843268, label %597
    i64 66053, label %597
    i64 66054, label %597
    i64 16843524, label %745
    i64 66309, label %745
    i64 66310, label %745
    i64 0, label %871
    i64 1, label %900
    i64 2, label %929
    i64 3, label %964
  ]

; <label>:116:                                    ; preds = %103
  %117 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %118 = load i32, i32* %67, align 4
  %119 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %120 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %119, i32 0, i32 12
  store %struct.ttf_reader* %117, %struct.ttf_reader** %48, align 8
  store i32 %118, i32* %49, align 4
  store i64* %62, i64** %50, align 8
  store i8* %63, i8** %51, align 8
  store i64* %120, i64** %52, align 8
  store i32 210698240, i32* %53, align 4
  %121 = load i32, i32* %49, align 4
  %122 = bitcast %union.anon* %55 to i32*
  store i32 %121, i32* %122, align 4
  %123 = bitcast %union.anon* %55 to %struct.anon*
  %124 = bitcast %struct.anon* %123 to i32*
  %125 = load i32, i32* %124, align 4
  %126 = lshr i32 %125, 28
  %127 = icmp eq i32 %126, 15
  br i1 %127, label %128, label %165

; <label>:128:                                    ; preds = %116
  %129 = bitcast %union.anon* %55 to %struct.anon*
  %130 = bitcast %struct.anon* %129 to i32*
  %131 = load i32, i32* %130, align 4
  %132 = and i32 %131, 268435455
  %133 = and i32 %132, 15
  store i32 %133, i32* %56, align 4
  %134 = load i32, i32* %56, align 4
  %135 = icmp eq i32 %134, 0
  br i1 %135, label %136, label %140

; <label>:136:                                    ; preds = %128
  %137 = load i64*, i64** %52, align 8
  %138 = load i64, i64* %137, align 8
  %139 = add nsw i64 %138, 210698240
  store i64 %139, i64* %137, align 8
  br label %164

; <label>:140:                                    ; preds = %128
  %141 = load i64*, i64** %52, align 8
  %142 = load i64, i64* %141, align 8
  %143 = bitcast %union.anon* %55 to %struct.anon*
  %144 = bitcast %struct.anon* %143 to i32*
  %145 = load i32, i32* %144, align 4
  %146 = and i32 %145, 268435455
  %147 = zext i32 %146 to i64
  %148 = add nsw i64 %142, %147
  store i64 %148, i64* %54, align 8
  %149 = load i64, i64* %54, align 8
  %150 = load %struct.ttf_reader*, %struct.ttf_reader** %48, align 8
  %151 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %150, i32 0, i32 2
  %152 = load i64, i64* %151, align 8
  %153 = mul nsw i64 %149, %152
  %154 = load i64*, i64** %50, align 8
  store i64 %153, i64* %154, align 8
  %155 = load %struct.ttf_reader*, %struct.ttf_reader** %48, align 8
  %156 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %155, i32 0, i32 9
  %157 = load i64, i64* %156, align 8
  %158 = load i32, i32* %56, align 4
  %159 = call i32 @llvm.cttz.i32(i32 %158, i1 true)
  %160 = sext i32 %159 to i64
  %161 = add nsw i64 %157, %160
  %162 = trunc i64 %161 to i8
  %163 = load i8*, i8** %51, align 8
  store i8 %162, i8* %163, align 1
  br label %164

; <label>:164:                                    ; preds = %140, %136
  br label %207

; <label>:165:                                    ; preds = %116
  %166 = bitcast %union.anon* %55 to %struct.anon*
  %167 = bitcast %struct.anon* %166 to i32*
  %168 = load i32, i32* %167, align 4
  %169 = lshr i32 %168, 28
  %170 = icmp sgt i32 %169, 4
  br i1 %170, label %171, label %181

; <label>:171:                                    ; preds = %165
  %172 = bitcast %union.anon* %55 to %struct.anon*
  %173 = bitcast %struct.anon* %172 to i32*
  %174 = load i32, i32* %173, align 4
  %175 = lshr i32 %174, 28
  %176 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.str, i32 0, i32 0), i32 %175)
  %177 = sext i32 %176 to i64
  store i64 %177, i64* @order_gurantee, align 8
  br label %178

; <label>:178:                                    ; preds = %178, %171
  %179 = load i64, i64* @order_gurantee, align 8
  %180 = add nsw i64 %179, 1
  store i64 %180, i64* @order_gurantee, align 8
  br label %178

; <label>:181:                                    ; preds = %165
  %182 = load i64*, i64** %52, align 8
  %183 = load i64, i64* %182, align 8
  %184 = bitcast %union.anon* %55 to %struct.anon*
  %185 = bitcast %struct.anon* %184 to i32*
  %186 = load i32, i32* %185, align 4
  %187 = and i32 %186, 268435455
  %188 = zext i32 %187 to i64
  %189 = add nsw i64 %183, %188
  store i64 %189, i64* %54, align 8
  %190 = load i64, i64* %54, align 8
  %191 = load %struct.ttf_reader*, %struct.ttf_reader** %48, align 8
  %192 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %191, i32 0, i32 2
  %193 = load i64, i64* %192, align 8
  %194 = mul nsw i64 %190, %193
  %195 = load i64*, i64** %50, align 8
  store i64 %194, i64* %195, align 8
  %196 = load %struct.ttf_reader*, %struct.ttf_reader** %48, align 8
  %197 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %196, i32 0, i32 8
  %198 = load i64, i64* %197, align 8
  %199 = bitcast %union.anon* %55 to %struct.anon*
  %200 = bitcast %struct.anon* %199 to i32*
  %201 = load i32, i32* %200, align 4
  %202 = lshr i32 %201, 28
  %203 = zext i32 %202 to i64
  %204 = add nsw i64 %198, %203
  %205 = trunc i64 %204 to i8
  %206 = load i8*, i8** %51, align 8
  store i8 %205, i8* %206, align 1
  br label %207

; <label>:207:                                    ; preds = %164, %181
  br label %1061

; <label>:208:                                    ; preds = %103
  %209 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %210 = load i32, i32* %67, align 4
  %211 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %212 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %211, i32 0, i32 12
  store %struct.ttf_reader* %209, %struct.ttf_reader** %40, align 8
  store i32 %210, i32* %41, align 4
  store i64* %62, i64** %42, align 8
  store i8* %63, i8** %43, align 8
  store i64* %212, i64** %44, align 8
  store i32 65536, i32* %46, align 4
  %213 = load i32, i32* %41, align 4
  %214 = bitcast %union.anon.2* %47 to i32*
  store i32 %213, i32* %214, align 4
  %215 = bitcast %union.anon.2* %47 to %struct.anon.3*
  %216 = bitcast %struct.anon.3* %215 to i32*
  %217 = load i32, i32* %216, align 4
  %218 = lshr i32 %217, 28
  %219 = icmp eq i32 %218, 15
  br i1 %219, label %220, label %263

; <label>:220:                                    ; preds = %208
  %221 = bitcast %union.anon.2* %47 to %struct.anon.4*
  %222 = bitcast %struct.anon.4* %221 to i32*
  %223 = load i32, i32* %222, align 4
  %224 = lshr i32 %223, 16
  %225 = and i32 %224, 4095
  %226 = icmp eq i32 %225, 0
  br i1 %226, label %227, label %231

; <label>:227:                                    ; preds = %220
  %228 = load i64*, i64** %44, align 8
  %229 = load i64, i64* %228, align 8
  %230 = add nsw i64 %229, 65536
  store i64 %230, i64* %228, align 8
  br label %262

; <label>:231:                                    ; preds = %220
  %232 = load i64*, i64** %44, align 8
  %233 = load i64, i64* %232, align 8
  %234 = bitcast %union.anon.2* %47 to %struct.anon.3*
  %235 = bitcast %struct.anon.3* %234 to i32*
  %236 = load i32, i32* %235, align 4
  %237 = and i32 %236, 65535
  %238 = zext i32 %237 to i64
  %239 = add nsw i64 %233, %238
  store i64 %239, i64* %45, align 8
  %240 = load i64, i64* %45, align 8
  %241 = load %struct.ttf_reader*, %struct.ttf_reader** %40, align 8
  %242 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %241, i32 0, i32 4
  %243 = load i64, i64* %242, align 8
  %244 = mul nsw i64 %240, %243
  %245 = load %struct.ttf_reader*, %struct.ttf_reader** %40, align 8
  %246 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %245, i32 0, i32 3
  %247 = load i64, i64* %246, align 8
  %248 = load i64*, i64** %42, align 8
  store i64 %244, i64* %248, align 8
  %249 = load %struct.ttf_reader*, %struct.ttf_reader** %40, align 8
  %250 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %249, i32 0, i32 9
  %251 = load i64, i64* %250, align 8
  %252 = bitcast %union.anon.2* %47 to %struct.anon.4*
  %253 = bitcast %struct.anon.4* %252 to i32*
  %254 = load i32, i32* %253, align 4
  %255 = lshr i32 %254, 16
  %256 = and i32 %255, 4095
  %257 = call i32 @llvm.cttz.i32(i32 %256, i1 true)
  %258 = sext i32 %257 to i64
  %259 = add nsw i64 %251, %258
  %260 = trunc i64 %259 to i8
  %261 = load i8*, i8** %43, align 8
  store i8 %260, i8* %261, align 1
  br label %262

; <label>:262:                                    ; preds = %231, %227
  br label %322

; <label>:263:                                    ; preds = %208
  %264 = bitcast %union.anon.2* %47 to %struct.anon.3*
  %265 = bitcast %struct.anon.3* %264 to i32*
  %266 = load i32, i32* %265, align 4
  %267 = lshr i32 %266, 28
  %268 = icmp eq i32 %267, 0
  br i1 %268, label %275, label %269

; <label>:269:                                    ; preds = %263
  %270 = bitcast %union.anon.2* %47 to %struct.anon.3*
  %271 = bitcast %struct.anon.3* %270 to i32*
  %272 = load i32, i32* %271, align 4
  %273 = lshr i32 %272, 28
  %274 = icmp sgt i32 %273, 4
  br i1 %274, label %275, label %285

; <label>:275:                                    ; preds = %269, %263
  %276 = bitcast %union.anon.2* %47 to %struct.anon.3*
  %277 = bitcast %struct.anon.3* %276 to i32*
  %278 = load i32, i32* %277, align 4
  %279 = lshr i32 %278, 28
  %280 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([40 x i8], [40 x i8]* @.str.1, i32 0, i32 0), i32 %279)
  %281 = sext i32 %280 to i64
  store i64 %281, i64* @order_gurantee, align 8
  br label %282

; <label>:282:                                    ; preds = %282, %275
  %283 = load i64, i64* @order_gurantee, align 8
  %284 = add nsw i64 %283, 1
  store i64 %284, i64* @order_gurantee, align 8
  br label %282

; <label>:285:                                    ; preds = %269
  %286 = load i64*, i64** %44, align 8
  %287 = load i64, i64* %286, align 8
  %288 = bitcast %union.anon.2* %47 to %struct.anon.3*
  %289 = bitcast %struct.anon.3* %288 to i32*
  %290 = load i32, i32* %289, align 4
  %291 = and i32 %290, 65535
  %292 = zext i32 %291 to i64
  %293 = add nsw i64 %287, %292
  store i64 %293, i64* %45, align 8
  %294 = load i64, i64* %45, align 8
  %295 = load %struct.ttf_reader*, %struct.ttf_reader** %40, align 8
  %296 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %295, i32 0, i32 4
  %297 = load i64, i64* %296, align 8
  %298 = mul nsw i64 %294, %297
  %299 = bitcast %union.anon.2* %47 to %struct.anon.3*
  %300 = bitcast %struct.anon.3* %299 to i32*
  %301 = load i32, i32* %300, align 4
  %302 = lshr i32 %301, 16
  %303 = and i32 %302, 4095
  %304 = zext i32 %303 to i64
  %305 = load %struct.ttf_reader*, %struct.ttf_reader** %40, align 8
  %306 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %305, i32 0, i32 3
  %307 = load i64, i64* %306, align 8
  %308 = mul nsw i64 %304, %307
  %309 = add nsw i64 %298, %308
  %310 = load i64*, i64** %42, align 8
  store i64 %309, i64* %310, align 8
  %311 = load %struct.ttf_reader*, %struct.ttf_reader** %40, align 8
  %312 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %311, i32 0, i32 8
  %313 = load i64, i64* %312, align 8
  %314 = bitcast %union.anon.2* %47 to %struct.anon.3*
  %315 = bitcast %struct.anon.3* %314 to i32*
  %316 = load i32, i32* %315, align 4
  %317 = lshr i32 %316, 28
  %318 = zext i32 %317 to i64
  %319 = add nsw i64 %313, %318
  %320 = trunc i64 %319 to i8
  %321 = load i8*, i8** %43, align 8
  store i8 %320, i8* %321, align 1
  br label %322

; <label>:322:                                    ; preds = %262, %285
  br label %1061

; <label>:323:                                    ; preds = %103
  %324 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %325 = load i32, i32* %67, align 4
  %326 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %327 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %326, i32 0, i32 12
  store %struct.ttf_reader* %324, %struct.ttf_reader** %30, align 8
  store i32 %325, i32* %31, align 4
  store i32 1, i32* %32, align 4
  store i64* %62, i64** %33, align 8
  store i8* %63, i8** %34, align 8
  store i64* %327, i64** %35, align 8
  store i32 33552000, i32* %37, align 4
  store i32 33554432, i32* %38, align 4
  %328 = load i32, i32* %31, align 4
  %329 = zext i32 %328 to i64
  %330 = bitcast %union.anon.0* %39 to i64*
  store i64 %329, i64* %330, align 8
  %331 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %332 = bitcast %struct.anon.1* %331 to i32*
  %333 = load i32, i32* %332, align 8
  %334 = lshr i32 %333, 31
  %335 = icmp eq i32 %334, 1
  br i1 %335, label %336, label %442

; <label>:336:                                    ; preds = %323
  %337 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %338 = bitcast %struct.anon.1* %337 to i32*
  %339 = load i32, i32* %338, align 8
  %340 = lshr i32 %339, 25
  %341 = and i32 %340, 63
  %342 = icmp eq i32 %341, 63
  br i1 %342, label %343, label %372

; <label>:343:                                    ; preds = %336
  %344 = load i32, i32* %32, align 4
  %345 = icmp eq i32 %344, 1
  br i1 %345, label %346, label %350

; <label>:346:                                    ; preds = %343
  %347 = load i64*, i64** %35, align 8
  %348 = load i64, i64* %347, align 8
  %349 = add i64 %348, 33552000
  store i64 %349, i64* %347, align 8
  br label %371

; <label>:350:                                    ; preds = %343
  %351 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %352 = bitcast %struct.anon.1* %351 to i32*
  %353 = load i32, i32* %352, align 8
  %354 = and i32 %353, 33554431
  %355 = icmp eq i32 %354, 0
  br i1 %355, label %356, label %360

; <label>:356:                                    ; preds = %350
  %357 = load i64*, i64** %35, align 8
  %358 = load i64, i64* %357, align 8
  %359 = add i64 %358, 33554432
  store i64 %359, i64* %357, align 8
  br label %370

; <label>:360:                                    ; preds = %350
  %361 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %362 = bitcast %struct.anon.1* %361 to i32*
  %363 = load i32, i32* %362, align 8
  %364 = and i32 %363, 33554431
  %365 = zext i32 %364 to i64
  %366 = mul i64 33554432, %365
  %367 = load i64*, i64** %35, align 8
  %368 = load i64, i64* %367, align 8
  %369 = add i64 %368, %366
  store i64 %369, i64* %367, align 8
  br label %370

; <label>:370:                                    ; preds = %360, %356
  br label %371

; <label>:371:                                    ; preds = %370, %346
  br label %372

; <label>:372:                                    ; preds = %371, %336
  %373 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %374 = bitcast %struct.anon.1* %373 to i32*
  %375 = load i32, i32* %374, align 8
  %376 = lshr i32 %375, 25
  %377 = and i32 %376, 63
  %378 = icmp sge i32 %377, 1
  br i1 %378, label %379, label %414

; <label>:379:                                    ; preds = %372
  %380 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %381 = bitcast %struct.anon.1* %380 to i32*
  %382 = load i32, i32* %381, align 8
  %383 = lshr i32 %382, 25
  %384 = and i32 %383, 63
  %385 = icmp sle i32 %384, 15
  br i1 %385, label %386, label %414

; <label>:386:                                    ; preds = %379
  %387 = load i64*, i64** %35, align 8
  %388 = load i64, i64* %387, align 8
  %389 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %390 = bitcast %struct.anon.1* %389 to i32*
  %391 = load i32, i32* %390, align 8
  %392 = and i32 %391, 33554431
  %393 = zext i32 %392 to i64
  %394 = add nsw i64 %388, %393
  store i64 %394, i64* %36, align 8
  %395 = load i64, i64* %36, align 8
  %396 = load %struct.ttf_reader*, %struct.ttf_reader** %30, align 8
  %397 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %396, i32 0, i32 2
  %398 = load i64, i64* %397, align 8
  %399 = mul nsw i64 %395, %398
  %400 = load i64*, i64** %33, align 8
  store i64 %399, i64* %400, align 8
  %401 = load %struct.ttf_reader*, %struct.ttf_reader** %30, align 8
  %402 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %401, i32 0, i32 9
  %403 = load i64, i64* %402, align 8
  %404 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %405 = bitcast %struct.anon.1* %404 to i32*
  %406 = load i32, i32* %405, align 8
  %407 = lshr i32 %406, 25
  %408 = and i32 %407, 63
  %409 = call i32 @llvm.cttz.i32(i32 %408, i1 true) #4
  %410 = sext i32 %409 to i64
  %411 = add nsw i64 %403, %410
  %412 = trunc i64 %411 to i8
  %413 = load i8*, i8** %34, align 8
  store i8 %412, i8* %413, align 1
  br label %414

; <label>:414:                                    ; preds = %386, %379, %372
  %415 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %416 = bitcast %struct.anon.1* %415 to i32*
  %417 = load i32, i32* %416, align 8
  %418 = lshr i32 %417, 25
  %419 = and i32 %418, 63
  %420 = icmp eq i32 %419, 0
  br i1 %420, label %421, label %441

; <label>:421:                                    ; preds = %414
  %422 = load i64*, i64** %35, align 8
  %423 = load i64, i64* %422, align 8
  %424 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %425 = bitcast %struct.anon.1* %424 to i32*
  %426 = load i32, i32* %425, align 8
  %427 = and i32 %426, 33554431
  %428 = zext i32 %427 to i64
  %429 = add nsw i64 %423, %428
  store i64 %429, i64* %36, align 8
  %430 = load i64, i64* %36, align 8
  %431 = load %struct.ttf_reader*, %struct.ttf_reader** %30, align 8
  %432 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %431, i32 0, i32 2
  %433 = load i64, i64* %432, align 8
  %434 = mul nsw i64 %430, %433
  %435 = load i64*, i64** %33, align 8
  store i64 %434, i64* %435, align 8
  %436 = load %struct.ttf_reader*, %struct.ttf_reader** %30, align 8
  %437 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %436, i32 0, i32 8
  %438 = load i64, i64* %437, align 8
  %439 = trunc i64 %438 to i8
  %440 = load i8*, i8** %34, align 8
  store i8 %439, i8* %440, align 1
  br label %441

; <label>:441:                                    ; preds = %421, %414
  br label %470

; <label>:442:                                    ; preds = %323
  %443 = load i64*, i64** %35, align 8
  %444 = load i64, i64* %443, align 8
  %445 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %446 = bitcast %struct.anon.1* %445 to i32*
  %447 = load i32, i32* %446, align 8
  %448 = and i32 %447, 33554431
  %449 = zext i32 %448 to i64
  %450 = add nsw i64 %444, %449
  store i64 %450, i64* %36, align 8
  %451 = load i64, i64* %36, align 8
  %452 = load %struct.ttf_reader*, %struct.ttf_reader** %30, align 8
  %453 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %452, i32 0, i32 2
  %454 = load i64, i64* %453, align 8
  %455 = mul nsw i64 %451, %454
  %456 = load i64*, i64** %33, align 8
  store i64 %455, i64* %456, align 8
  %457 = load %struct.ttf_reader*, %struct.ttf_reader** %30, align 8
  %458 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %457, i32 0, i32 8
  %459 = load i64, i64* %458, align 8
  %460 = bitcast %union.anon.0* %39 to %struct.anon.1*
  %461 = bitcast %struct.anon.1* %460 to i32*
  %462 = load i32, i32* %461, align 8
  %463 = lshr i32 %462, 25
  %464 = and i32 %463, 63
  %465 = zext i32 %464 to i64
  %466 = add nsw i64 %459, %465
  %467 = add nsw i64 %466, 1
  %468 = trunc i64 %467 to i8
  %469 = load i8*, i8** %34, align 8
  store i8 %468, i8* %469, align 1
  br label %470

; <label>:470:                                    ; preds = %441, %442
  br label %1061

; <label>:471:                                    ; preds = %103
  %472 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %473 = load i32, i32* %67, align 4
  %474 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %475 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %474, i32 0, i32 12
  store %struct.ttf_reader* %472, %struct.ttf_reader** %4, align 8
  store i32 %473, i32* %5, align 4
  store i32 1, i32* %6, align 4
  store i64* %62, i64** %7, align 8
  store i8* %63, i8** %8, align 8
  store i64* %475, i64** %9, align 8
  store i32 1024, i32* %10, align 4
  %476 = load i32, i32* %5, align 4
  %477 = bitcast %union.anon.5* %11 to i32*
  store i32 %476, i32* %477, align 4
  %478 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %479 = bitcast %struct.anon.6* %478 to i32*
  %480 = load i32, i32* %479, align 4
  %481 = lshr i32 %480, 31
  %482 = icmp eq i32 %481, 1
  br i1 %482, label %483, label %559

; <label>:483:                                    ; preds = %471
  %484 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %485 = bitcast %struct.anon.6* %484 to i32*
  %486 = load i32, i32* %485, align 4
  %487 = lshr i32 %486, 25
  %488 = and i32 %487, 63
  %489 = icmp eq i32 %488, 63
  br i1 %489, label %490, label %514

; <label>:490:                                    ; preds = %483
  %491 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %492 = bitcast %struct.anon.6* %491 to i32*
  %493 = load i32, i32* %492, align 4
  %494 = and i32 %493, 1023
  %495 = icmp eq i32 %494, 0
  br i1 %495, label %499, label %496

; <label>:496:                                    ; preds = %490
  %497 = load i32, i32* %6, align 4
  %498 = icmp eq i32 %497, 1
  br i1 %498, label %499, label %503

; <label>:499:                                    ; preds = %496, %490
  %500 = load i64*, i64** %9, align 8
  %501 = load i64, i64* %500, align 8
  %502 = add i64 %501, 1024
  store i64 %502, i64* %500, align 8
  br label %513

; <label>:503:                                    ; preds = %496
  %504 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %505 = bitcast %struct.anon.6* %504 to i32*
  %506 = load i32, i32* %505, align 4
  %507 = and i32 %506, 1023
  %508 = zext i32 %507 to i64
  %509 = mul i64 1024, %508
  %510 = load i64*, i64** %9, align 8
  %511 = load i64, i64* %510, align 8
  %512 = add i64 %511, %509
  store i64 %512, i64* %510, align 8
  br label %513

; <label>:513:                                    ; preds = %503, %499
  br label %514

; <label>:514:                                    ; preds = %513, %483
  %515 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %516 = bitcast %struct.anon.6* %515 to i32*
  %517 = load i32, i32* %516, align 4
  %518 = lshr i32 %517, 25
  %519 = and i32 %518, 63
  %520 = icmp sge i32 %519, 1
  br i1 %520, label %521, label %558

; <label>:521:                                    ; preds = %514
  %522 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %523 = bitcast %struct.anon.6* %522 to i32*
  %524 = load i32, i32* %523, align 4
  %525 = lshr i32 %524, 25
  %526 = and i32 %525, 63
  %527 = icmp sle i32 %526, 15
  br i1 %527, label %528, label %558

; <label>:528:                                    ; preds = %521
  %529 = load i64*, i64** %9, align 8
  %530 = load i64, i64* %529, align 8
  %531 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %532 = bitcast %struct.anon.6* %531 to i32*
  %533 = load i32, i32* %532, align 4
  %534 = and i32 %533, 1023
  %535 = zext i32 %534 to i64
  %536 = add nsw i64 %530, %535
  %537 = load %struct.ttf_reader*, %struct.ttf_reader** %4, align 8
  %538 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %537, i32 0, i32 4
  %539 = load i64, i64* %538, align 8
  %540 = mul nsw i64 %536, %539
  %541 = load %struct.ttf_reader*, %struct.ttf_reader** %4, align 8
  %542 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %541, i32 0, i32 3
  %543 = load i64, i64* %542, align 8
  %544 = load i64*, i64** %7, align 8
  store i64 %540, i64* %544, align 8
  %545 = load %struct.ttf_reader*, %struct.ttf_reader** %4, align 8
  %546 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %545, i32 0, i32 9
  %547 = load i64, i64* %546, align 8
  %548 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %549 = bitcast %struct.anon.6* %548 to i32*
  %550 = load i32, i32* %549, align 4
  %551 = lshr i32 %550, 25
  %552 = and i32 %551, 63
  %553 = call i32 @llvm.cttz.i32(i32 %552, i1 true) #4
  %554 = sext i32 %553 to i64
  %555 = add nsw i64 %547, %554
  %556 = trunc i64 %555 to i8
  %557 = load i8*, i8** %8, align 8
  store i8 %556, i8* %557, align 1
  br label %558

; <label>:558:                                    ; preds = %528, %521, %514
  br label %596

; <label>:559:                                    ; preds = %471
  %560 = load i64*, i64** %9, align 8
  %561 = load i64, i64* %560, align 8
  %562 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %563 = bitcast %struct.anon.6* %562 to i32*
  %564 = load i32, i32* %563, align 4
  %565 = and i32 %564, 1023
  %566 = zext i32 %565 to i64
  %567 = add nsw i64 %561, %566
  %568 = load %struct.ttf_reader*, %struct.ttf_reader** %4, align 8
  %569 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %568, i32 0, i32 4
  %570 = load i64, i64* %569, align 8
  %571 = mul nsw i64 %567, %570
  %572 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %573 = bitcast %struct.anon.6* %572 to i32*
  %574 = load i32, i32* %573, align 4
  %575 = lshr i32 %574, 10
  %576 = and i32 %575, 32767
  %577 = zext i32 %576 to i64
  %578 = load %struct.ttf_reader*, %struct.ttf_reader** %4, align 8
  %579 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %578, i32 0, i32 3
  %580 = load i64, i64* %579, align 8
  %581 = mul nsw i64 %577, %580
  %582 = add nsw i64 %571, %581
  %583 = load i64*, i64** %7, align 8
  store i64 %582, i64* %583, align 8
  %584 = load %struct.ttf_reader*, %struct.ttf_reader** %4, align 8
  %585 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %584, i32 0, i32 8
  %586 = load i64, i64* %585, align 8
  %587 = bitcast %union.anon.5* %11 to %struct.anon.6*
  %588 = bitcast %struct.anon.6* %587 to i32*
  %589 = load i32, i32* %588, align 4
  %590 = lshr i32 %589, 25
  %591 = and i32 %590, 63
  %592 = zext i32 %591 to i64
  %593 = add nsw i64 %586, %592
  %594 = trunc i64 %593 to i8
  %595 = load i8*, i8** %8, align 8
  store i8 %594, i8* %595, align 1
  br label %596

; <label>:596:                                    ; preds = %558, %559
  br label %1061

; <label>:597:                                    ; preds = %103, %103, %103
  %598 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %599 = load i32, i32* %67, align 4
  %600 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %601 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %600, i32 0, i32 12
  store %struct.ttf_reader* %598, %struct.ttf_reader** %12, align 8
  store i32 %599, i32* %13, align 4
  store i32 2, i32* %14, align 4
  store i64* %62, i64** %15, align 8
  store i8* %63, i8** %16, align 8
  store i64* %601, i64** %17, align 8
  store i32 33552000, i32* %19, align 4
  store i32 33554432, i32* %20, align 4
  %602 = load i32, i32* %13, align 4
  %603 = zext i32 %602 to i64
  %604 = bitcast %union.anon.0* %21 to i64*
  store i64 %603, i64* %604, align 8
  %605 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %606 = bitcast %struct.anon.1* %605 to i32*
  %607 = load i32, i32* %606, align 8
  %608 = lshr i32 %607, 31
  %609 = icmp eq i32 %608, 1
  br i1 %609, label %610, label %716

; <label>:610:                                    ; preds = %597
  %611 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %612 = bitcast %struct.anon.1* %611 to i32*
  %613 = load i32, i32* %612, align 8
  %614 = lshr i32 %613, 25
  %615 = and i32 %614, 63
  %616 = icmp eq i32 %615, 63
  br i1 %616, label %617, label %646

; <label>:617:                                    ; preds = %610
  %618 = load i32, i32* %14, align 4
  %619 = icmp eq i32 %618, 1
  br i1 %619, label %620, label %624

; <label>:620:                                    ; preds = %617
  %621 = load i64*, i64** %17, align 8
  %622 = load i64, i64* %621, align 8
  %623 = add i64 %622, 33552000
  store i64 %623, i64* %621, align 8
  br label %645

; <label>:624:                                    ; preds = %617
  %625 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %626 = bitcast %struct.anon.1* %625 to i32*
  %627 = load i32, i32* %626, align 8
  %628 = and i32 %627, 33554431
  %629 = icmp eq i32 %628, 0
  br i1 %629, label %630, label %634

; <label>:630:                                    ; preds = %624
  %631 = load i64*, i64** %17, align 8
  %632 = load i64, i64* %631, align 8
  %633 = add i64 %632, 33554432
  store i64 %633, i64* %631, align 8
  br label %644

; <label>:634:                                    ; preds = %624
  %635 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %636 = bitcast %struct.anon.1* %635 to i32*
  %637 = load i32, i32* %636, align 8
  %638 = and i32 %637, 33554431
  %639 = zext i32 %638 to i64
  %640 = mul i64 33554432, %639
  %641 = load i64*, i64** %17, align 8
  %642 = load i64, i64* %641, align 8
  %643 = add i64 %642, %640
  store i64 %643, i64* %641, align 8
  br label %644

; <label>:644:                                    ; preds = %634, %630
  br label %645

; <label>:645:                                    ; preds = %644, %620
  br label %646

; <label>:646:                                    ; preds = %645, %610
  %647 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %648 = bitcast %struct.anon.1* %647 to i32*
  %649 = load i32, i32* %648, align 8
  %650 = lshr i32 %649, 25
  %651 = and i32 %650, 63
  %652 = icmp sge i32 %651, 1
  br i1 %652, label %653, label %688

; <label>:653:                                    ; preds = %646
  %654 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %655 = bitcast %struct.anon.1* %654 to i32*
  %656 = load i32, i32* %655, align 8
  %657 = lshr i32 %656, 25
  %658 = and i32 %657, 63
  %659 = icmp sle i32 %658, 15
  br i1 %659, label %660, label %688

; <label>:660:                                    ; preds = %653
  %661 = load i64*, i64** %17, align 8
  %662 = load i64, i64* %661, align 8
  %663 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %664 = bitcast %struct.anon.1* %663 to i32*
  %665 = load i32, i32* %664, align 8
  %666 = and i32 %665, 33554431
  %667 = zext i32 %666 to i64
  %668 = add nsw i64 %662, %667
  store i64 %668, i64* %18, align 8
  %669 = load i64, i64* %18, align 8
  %670 = load %struct.ttf_reader*, %struct.ttf_reader** %12, align 8
  %671 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %670, i32 0, i32 2
  %672 = load i64, i64* %671, align 8
  %673 = mul nsw i64 %669, %672
  %674 = load i64*, i64** %15, align 8
  store i64 %673, i64* %674, align 8
  %675 = load %struct.ttf_reader*, %struct.ttf_reader** %12, align 8
  %676 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %675, i32 0, i32 9
  %677 = load i64, i64* %676, align 8
  %678 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %679 = bitcast %struct.anon.1* %678 to i32*
  %680 = load i32, i32* %679, align 8
  %681 = lshr i32 %680, 25
  %682 = and i32 %681, 63
  %683 = call i32 @llvm.cttz.i32(i32 %682, i1 true) #4
  %684 = sext i32 %683 to i64
  %685 = add nsw i64 %677, %684
  %686 = trunc i64 %685 to i8
  %687 = load i8*, i8** %16, align 8
  store i8 %686, i8* %687, align 1
  br label %688

; <label>:688:                                    ; preds = %660, %653, %646
  %689 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %690 = bitcast %struct.anon.1* %689 to i32*
  %691 = load i32, i32* %690, align 8
  %692 = lshr i32 %691, 25
  %693 = and i32 %692, 63
  %694 = icmp eq i32 %693, 0
  br i1 %694, label %695, label %715

; <label>:695:                                    ; preds = %688
  %696 = load i64*, i64** %17, align 8
  %697 = load i64, i64* %696, align 8
  %698 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %699 = bitcast %struct.anon.1* %698 to i32*
  %700 = load i32, i32* %699, align 8
  %701 = and i32 %700, 33554431
  %702 = zext i32 %701 to i64
  %703 = add nsw i64 %697, %702
  store i64 %703, i64* %18, align 8
  %704 = load i64, i64* %18, align 8
  %705 = load %struct.ttf_reader*, %struct.ttf_reader** %12, align 8
  %706 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %705, i32 0, i32 2
  %707 = load i64, i64* %706, align 8
  %708 = mul nsw i64 %704, %707
  %709 = load i64*, i64** %15, align 8
  store i64 %708, i64* %709, align 8
  %710 = load %struct.ttf_reader*, %struct.ttf_reader** %12, align 8
  %711 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %710, i32 0, i32 8
  %712 = load i64, i64* %711, align 8
  %713 = trunc i64 %712 to i8
  %714 = load i8*, i8** %16, align 8
  store i8 %713, i8* %714, align 1
  br label %715

; <label>:715:                                    ; preds = %695, %688
  br label %744

; <label>:716:                                    ; preds = %597
  %717 = load i64*, i64** %17, align 8
  %718 = load i64, i64* %717, align 8
  %719 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %720 = bitcast %struct.anon.1* %719 to i32*
  %721 = load i32, i32* %720, align 8
  %722 = and i32 %721, 33554431
  %723 = zext i32 %722 to i64
  %724 = add nsw i64 %718, %723
  store i64 %724, i64* %18, align 8
  %725 = load i64, i64* %18, align 8
  %726 = load %struct.ttf_reader*, %struct.ttf_reader** %12, align 8
  %727 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %726, i32 0, i32 2
  %728 = load i64, i64* %727, align 8
  %729 = mul nsw i64 %725, %728
  %730 = load i64*, i64** %15, align 8
  store i64 %729, i64* %730, align 8
  %731 = load %struct.ttf_reader*, %struct.ttf_reader** %12, align 8
  %732 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %731, i32 0, i32 8
  %733 = load i64, i64* %732, align 8
  %734 = bitcast %union.anon.0* %21 to %struct.anon.1*
  %735 = bitcast %struct.anon.1* %734 to i32*
  %736 = load i32, i32* %735, align 8
  %737 = lshr i32 %736, 25
  %738 = and i32 %737, 63
  %739 = zext i32 %738 to i64
  %740 = add nsw i64 %733, %739
  %741 = add nsw i64 %740, 1
  %742 = trunc i64 %741 to i8
  %743 = load i8*, i8** %16, align 8
  store i8 %742, i8* %743, align 1
  br label %744

; <label>:744:                                    ; preds = %715, %716
  br label %1061

; <label>:745:                                    ; preds = %103, %103, %103
  %746 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %747 = load i32, i32* %67, align 4
  %748 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %749 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %748, i32 0, i32 12
  store %struct.ttf_reader* %746, %struct.ttf_reader** %22, align 8
  store i32 %747, i32* %23, align 4
  store i32 2, i32* %24, align 4
  store i64* %62, i64** %25, align 8
  store i8* %63, i8** %26, align 8
  store i64* %749, i64** %27, align 8
  store i32 1024, i32* %28, align 4
  %750 = load i32, i32* %23, align 4
  %751 = bitcast %union.anon.5* %29 to i32*
  store i32 %750, i32* %751, align 4
  %752 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %753 = bitcast %struct.anon.6* %752 to i32*
  %754 = load i32, i32* %753, align 4
  %755 = lshr i32 %754, 31
  %756 = icmp eq i32 %755, 1
  br i1 %756, label %757, label %833

; <label>:757:                                    ; preds = %745
  %758 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %759 = bitcast %struct.anon.6* %758 to i32*
  %760 = load i32, i32* %759, align 4
  %761 = lshr i32 %760, 25
  %762 = and i32 %761, 63
  %763 = icmp eq i32 %762, 63
  br i1 %763, label %764, label %788

; <label>:764:                                    ; preds = %757
  %765 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %766 = bitcast %struct.anon.6* %765 to i32*
  %767 = load i32, i32* %766, align 4
  %768 = and i32 %767, 1023
  %769 = icmp eq i32 %768, 0
  br i1 %769, label %773, label %770

; <label>:770:                                    ; preds = %764
  %771 = load i32, i32* %24, align 4
  %772 = icmp eq i32 %771, 1
  br i1 %772, label %773, label %777

; <label>:773:                                    ; preds = %770, %764
  %774 = load i64*, i64** %27, align 8
  %775 = load i64, i64* %774, align 8
  %776 = add i64 %775, 1024
  store i64 %776, i64* %774, align 8
  br label %787

; <label>:777:                                    ; preds = %770
  %778 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %779 = bitcast %struct.anon.6* %778 to i32*
  %780 = load i32, i32* %779, align 4
  %781 = and i32 %780, 1023
  %782 = zext i32 %781 to i64
  %783 = mul i64 1024, %782
  %784 = load i64*, i64** %27, align 8
  %785 = load i64, i64* %784, align 8
  %786 = add i64 %785, %783
  store i64 %786, i64* %784, align 8
  br label %787

; <label>:787:                                    ; preds = %777, %773
  br label %788

; <label>:788:                                    ; preds = %787, %757
  %789 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %790 = bitcast %struct.anon.6* %789 to i32*
  %791 = load i32, i32* %790, align 4
  %792 = lshr i32 %791, 25
  %793 = and i32 %792, 63
  %794 = icmp sge i32 %793, 1
  br i1 %794, label %795, label %832

; <label>:795:                                    ; preds = %788
  %796 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %797 = bitcast %struct.anon.6* %796 to i32*
  %798 = load i32, i32* %797, align 4
  %799 = lshr i32 %798, 25
  %800 = and i32 %799, 63
  %801 = icmp sle i32 %800, 15
  br i1 %801, label %802, label %832

; <label>:802:                                    ; preds = %795
  %803 = load i64*, i64** %27, align 8
  %804 = load i64, i64* %803, align 8
  %805 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %806 = bitcast %struct.anon.6* %805 to i32*
  %807 = load i32, i32* %806, align 4
  %808 = and i32 %807, 1023
  %809 = zext i32 %808 to i64
  %810 = add nsw i64 %804, %809
  %811 = load %struct.ttf_reader*, %struct.ttf_reader** %22, align 8
  %812 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %811, i32 0, i32 4
  %813 = load i64, i64* %812, align 8
  %814 = mul nsw i64 %810, %813
  %815 = load %struct.ttf_reader*, %struct.ttf_reader** %22, align 8
  %816 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %815, i32 0, i32 3
  %817 = load i64, i64* %816, align 8
  %818 = load i64*, i64** %25, align 8
  store i64 %814, i64* %818, align 8
  %819 = load %struct.ttf_reader*, %struct.ttf_reader** %22, align 8
  %820 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %819, i32 0, i32 9
  %821 = load i64, i64* %820, align 8
  %822 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %823 = bitcast %struct.anon.6* %822 to i32*
  %824 = load i32, i32* %823, align 4
  %825 = lshr i32 %824, 25
  %826 = and i32 %825, 63
  %827 = call i32 @llvm.cttz.i32(i32 %826, i1 true) #4
  %828 = sext i32 %827 to i64
  %829 = add nsw i64 %821, %828
  %830 = trunc i64 %829 to i8
  %831 = load i8*, i8** %26, align 8
  store i8 %830, i8* %831, align 1
  br label %832

; <label>:832:                                    ; preds = %802, %795, %788
  br label %870

; <label>:833:                                    ; preds = %745
  %834 = load i64*, i64** %27, align 8
  %835 = load i64, i64* %834, align 8
  %836 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %837 = bitcast %struct.anon.6* %836 to i32*
  %838 = load i32, i32* %837, align 4
  %839 = and i32 %838, 1023
  %840 = zext i32 %839 to i64
  %841 = add nsw i64 %835, %840
  %842 = load %struct.ttf_reader*, %struct.ttf_reader** %22, align 8
  %843 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %842, i32 0, i32 4
  %844 = load i64, i64* %843, align 8
  %845 = mul nsw i64 %841, %844
  %846 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %847 = bitcast %struct.anon.6* %846 to i32*
  %848 = load i32, i32* %847, align 4
  %849 = lshr i32 %848, 10
  %850 = and i32 %849, 32767
  %851 = zext i32 %850 to i64
  %852 = load %struct.ttf_reader*, %struct.ttf_reader** %22, align 8
  %853 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %852, i32 0, i32 3
  %854 = load i64, i64* %853, align 8
  %855 = mul nsw i64 %851, %854
  %856 = add nsw i64 %845, %855
  %857 = load i64*, i64** %25, align 8
  store i64 %856, i64* %857, align 8
  %858 = load %struct.ttf_reader*, %struct.ttf_reader** %22, align 8
  %859 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %858, i32 0, i32 8
  %860 = load i64, i64* %859, align 8
  %861 = bitcast %union.anon.5* %29 to %struct.anon.6*
  %862 = bitcast %struct.anon.6* %861 to i32*
  %863 = load i32, i32* %862, align 4
  %864 = lshr i32 %863, 25
  %865 = and i32 %864, 63
  %866 = zext i32 %865 to i64
  %867 = add nsw i64 %860, %866
  %868 = trunc i64 %867 to i8
  %869 = load i8*, i8** %26, align 8
  store i8 %868, i8* %869, align 1
  br label %870

; <label>:870:                                    ; preds = %832, %833
  br label %1061

; <label>:871:                                    ; preds = %103
  %872 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %873 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %872, i32 0, i32 14
  %874 = load i8*, i8** %873, align 8
  %875 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %876 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %875, i32 0, i32 11
  %877 = load i64, i64* %876, align 8
  %878 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %879 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %878, i32 0, i32 5
  %880 = load i64, i64* %879, align 8
  %881 = mul nsw i64 %877, %880
  %882 = getelementptr inbounds i8, i8* %874, i64 %881
  %883 = bitcast i8* %882 to %struct.TTTRRecord*
  store %struct.TTTRRecord* %883, %struct.TTTRRecord** %69, align 8
  %884 = load %struct.TTTRRecord*, %struct.TTTRRecord** %69, align 8
  %885 = getelementptr inbounds %struct.TTTRRecord, %struct.TTTRRecord* %884, i32 0, i32 0
  %886 = load i64, i64* %885, align 8
  %887 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %888 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %887, i32 0, i32 2
  %889 = load i64, i64* %888, align 8
  %890 = mul i64 %886, %889
  store i64 %890, i64* %62, align 8
  %891 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %892 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %891, i32 0, i32 8
  %893 = load i64, i64* %892, align 8
  %894 = load %struct.TTTRRecord*, %struct.TTTRRecord** %69, align 8
  %895 = getelementptr inbounds %struct.TTTRRecord, %struct.TTTRRecord* %894, i32 0, i32 1
  %896 = load i16, i16* %895, align 8
  %897 = zext i16 %896 to i64
  %898 = add nsw i64 %893, %897
  %899 = trunc i64 %898 to i8
  store i8 %899, i8* %63, align 1
  br label %1061

; <label>:900:                                    ; preds = %103
  %901 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %902 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %901, i32 0, i32 14
  %903 = load i8*, i8** %902, align 8
  %904 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %905 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %904, i32 0, i32 11
  %906 = load i64, i64* %905, align 8
  %907 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %908 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %907, i32 0, i32 5
  %909 = load i64, i64* %908, align 8
  %910 = mul nsw i64 %906, %909
  %911 = getelementptr inbounds i8, i8* %903, i64 %910
  %912 = bitcast i8* %911 to %struct.SITTTRStruct*
  store %struct.SITTTRStruct* %912, %struct.SITTTRStruct** %70, align 8
  %913 = load %struct.SITTTRStruct*, %struct.SITTTRStruct** %70, align 8
  %914 = getelementptr inbounds %struct.SITTTRStruct, %struct.SITTTRStruct* %913, i32 0, i32 2
  %915 = load i64, i64* %914, align 8
  %916 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %917 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %916, i32 0, i32 2
  %918 = load i64, i64* %917, align 8
  %919 = mul i64 %915, %918
  store i64 %919, i64* %62, align 8
  %920 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %921 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %920, i32 0, i32 8
  %922 = load i64, i64* %921, align 8
  %923 = load %struct.SITTTRStruct*, %struct.SITTTRStruct** %70, align 8
  %924 = getelementptr inbounds %struct.SITTTRStruct, %struct.SITTTRStruct* %923, i32 0, i32 1
  %925 = load i32, i32* %924, align 4
  %926 = sext i32 %925 to i64
  %927 = add nsw i64 %922, %926
  %928 = trunc i64 %927 to i8
  store i8 %928, i8* %63, align 1
  br label %1061

; <label>:929:                                    ; preds = %103
  %930 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %931 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %930, i32 0, i32 14
  %932 = load i8*, i8** %931, align 8
  %933 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %934 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %933, i32 0, i32 11
  %935 = load i64, i64* %934, align 8
  %936 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %937 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %936, i32 0, i32 5
  %938 = load i64, i64* %937, align 8
  %939 = mul nsw i64 %935, %938
  %940 = getelementptr inbounds i8, i8* %932, i64 %939
  %941 = bitcast i8* %940 to %union.COMPTTTRRecord*
  store %union.COMPTTTRRecord* %941, %union.COMPTTTRRecord** %71, align 8
  %942 = load %union.COMPTTTRRecord*, %union.COMPTTTRRecord** %71, align 8
  %943 = bitcast %union.COMPTTTRRecord* %942 to %struct.anon.7*
  %944 = bitcast %struct.anon.7* %943 to i64*
  %945 = load i64, i64* %944, align 8
  %946 = and i64 %945, 137438953471
  %947 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %948 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %947, i32 0, i32 2
  %949 = load i64, i64* %948, align 8
  %950 = mul i64 %946, %949
  store i64 %950, i64* %62, align 8
  %951 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %952 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %951, i32 0, i32 8
  %953 = load i64, i64* %952, align 8
  %954 = load %union.COMPTTTRRecord*, %union.COMPTTTRRecord** %71, align 8
  %955 = bitcast %union.COMPTTTRRecord* %954 to %struct.anon.7*
  %956 = bitcast %struct.anon.7* %955 to i64*
  %957 = load i64, i64* %956, align 8
  %958 = lshr i64 %957, 37
  %959 = and i64 %958, 7
  %960 = trunc i64 %959 to i32
  %961 = zext i32 %960 to i64
  %962 = add nsw i64 %953, %961
  %963 = trunc i64 %962 to i8
  store i8 %963, i8* %63, align 1
  br label %1061

; <label>:964:                                    ; preds = %103
  %965 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %966 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %965, i32 0, i32 14
  %967 = load i8*, i8** %966, align 8
  %968 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %969 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %968, i32 0, i32 11
  %970 = load i64, i64* %969, align 8
  %971 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %972 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %971, i32 0, i32 5
  %973 = load i64, i64* %972, align 8
  %974 = mul nsw i64 %970, %973
  %975 = getelementptr inbounds i8, i8* %967, i64 %974
  %976 = bitcast i8* %975 to %union.bh4bytesRec*
  store %union.bh4bytesRec* %976, %union.bh4bytesRec** %72, align 8
  %977 = load %union.bh4bytesRec*, %union.bh4bytesRec** %72, align 8
  %978 = bitcast %union.bh4bytesRec* %977 to %struct.anon.8*
  %979 = bitcast %struct.anon.8* %978 to i32*
  %980 = load i32, i32* %979, align 4
  %981 = and i32 %980, 4095
  %982 = zext i32 %981 to i64
  %983 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %984 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %983, i32 0, i32 12
  %985 = load i64, i64* %984, align 8
  %986 = add nsw i64 %982, %985
  %987 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %988 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %987, i32 0, i32 4
  %989 = load i64, i64* %988, align 8
  %990 = mul nsw i64 %986, %989
  %991 = load %union.bh4bytesRec*, %union.bh4bytesRec** %72, align 8
  %992 = bitcast %union.bh4bytesRec* %991 to %struct.anon.8*
  %993 = bitcast %struct.anon.8* %992 to i32*
  %994 = load i32, i32* %993, align 4
  %995 = lshr i32 %994, 16
  %996 = and i32 %995, 4095
  %997 = zext i32 %996 to i64
  %998 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %999 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %998, i32 0, i32 3
  %1000 = load i64, i64* %999, align 8
  %1001 = mul nsw i64 %997, %1000
  %1002 = add nsw i64 %990, %1001
  store i64 %1002, i64* %62, align 8
  %1003 = load %union.bh4bytesRec*, %union.bh4bytesRec** %72, align 8
  %1004 = bitcast %union.bh4bytesRec* %1003 to %struct.anon.8*
  %1005 = bitcast %struct.anon.8* %1004 to i32*
  %1006 = load i32, i32* %1005, align 4
  %1007 = lshr i32 %1006, 31
  %1008 = icmp ne i32 %1007, 0
  br i1 %1008, label %1009, label %1010

; <label>:1009:                                   ; preds = %964
  store i64 9223372036854775807, i64* %62, align 8
  br label %1010

; <label>:1010:                                   ; preds = %1009, %964
  %1011 = load %union.bh4bytesRec*, %union.bh4bytesRec** %72, align 8
  %1012 = bitcast %union.bh4bytesRec* %1011 to %struct.anon.8*
  %1013 = bitcast %struct.anon.8* %1012 to i32*
  %1014 = load i32, i32* %1013, align 4
  %1015 = lshr i32 %1014, 30
  %1016 = and i32 %1015, 1
  %1017 = icmp ne i32 %1016, 0
  br i1 %1017, label %1018, label %1023

; <label>:1018:                                   ; preds = %1010
  store i64 9223372036854775807, i64* %62, align 8
  %1019 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %1020 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %1019, i32 0, i32 12
  %1021 = load i64, i64* %1020, align 8
  %1022 = add nsw i64 %1021, 4096
  store i64 %1022, i64* %1020, align 8
  br label %1023

; <label>:1023:                                   ; preds = %1018, %1010
  %1024 = load %union.bh4bytesRec*, %union.bh4bytesRec** %72, align 8
  %1025 = bitcast %union.bh4bytesRec* %1024 to %struct.anon.8*
  %1026 = bitcast %struct.anon.8* %1025 to i32*
  %1027 = load i32, i32* %1026, align 4
  %1028 = lshr i32 %1027, 28
  %1029 = and i32 %1028, 1
  %1030 = icmp ne i32 %1029, 0
  br i1 %1030, label %1031, label %1044

; <label>:1031:                                   ; preds = %1023
  %1032 = load %union.bh4bytesRec*, %union.bh4bytesRec** %72, align 8
  %1033 = bitcast %union.bh4bytesRec* %1032 to %struct.anon.8*
  %1034 = bitcast %struct.anon.8* %1033 to i32*
  %1035 = load i32, i32* %1034, align 4
  %1036 = lshr i32 %1035, 12
  %1037 = and i32 %1036, 15
  %1038 = zext i32 %1037 to i64
  %1039 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %1040 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %1039, i32 0, i32 9
  %1041 = load i64, i64* %1040, align 8
  %1042 = add nsw i64 %1038, %1041
  %1043 = trunc i64 %1042 to i8
  store i8 %1043, i8* %63, align 1
  br label %1057

; <label>:1044:                                   ; preds = %1023
  %1045 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %1046 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %1045, i32 0, i32 8
  %1047 = load i64, i64* %1046, align 8
  %1048 = load %union.bh4bytesRec*, %union.bh4bytesRec** %72, align 8
  %1049 = bitcast %union.bh4bytesRec* %1048 to %struct.anon.8*
  %1050 = bitcast %struct.anon.8* %1049 to i32*
  %1051 = load i32, i32* %1050, align 4
  %1052 = lshr i32 %1051, 12
  %1053 = and i32 %1052, 15
  %1054 = zext i32 %1053 to i64
  %1055 = add nsw i64 %1047, %1054
  %1056 = trunc i64 %1055 to i8
  store i8 %1056, i8* %63, align 1
  br label %1057

; <label>:1057:                                   ; preds = %1044, %1031
  br label %1061

; <label>:1058:                                   ; preds = %103
  %1059 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([44 x i8], [44 x i8]* @.str.2, i32 0, i32 0))
  %1060 = sext i32 %1059 to i64
  store i64 %1060, i64* @order_gurantee, align 8
  br label %1061

; <label>:1061:                                   ; preds = %1058, %1057, %929, %900, %871, %870, %744, %596, %470, %322, %207
  %1062 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %1063 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %1062, i32 0, i32 11
  %1064 = load i64, i64* %1063, align 8
  %1065 = add nsw i64 %1064, 1
  store i64 %1065, i64* %1063, align 8
  %1066 = load i64, i64* %62, align 8
  %1067 = icmp eq i64 %1066, 9223372036854775807
  br i1 %1067, label %1068, label %1069

; <label>:1068:                                   ; preds = %1061
  br label %77

; <label>:1069:                                   ; preds = %1061
  %1070 = load i8, i8* %63, align 1
  %1071 = load i8*, i8** %60, align 8
  store i8 %1070, i8* %1071, align 1
  %1072 = load i64, i64* %62, align 8
  %1073 = load %struct.ttf_reader*, %struct.ttf_reader** %61, align 8
  %1074 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %1073, i32 0, i32 7
  %1075 = load i64, i64* %1074, align 8
  %1076 = add nsw i64 %1072, %1075
  store i64 %1076, i64* %57, align 8
  br label %1079

; <label>:1077:                                   ; preds = %102
  %1078 = load i8*, i8** %60, align 8
  store i8 -1, i8* %1078, align 1
  store i64 9223372036854775807, i64* %57, align 8
  br label %1079

; <label>:1079:                                   ; preds = %1077, %1069
  %1080 = load i64, i64* %57, align 8
  ret i64 %1080
}

; Function Attrs: alwaysinline nounwind uwtable
define dso_local i32 @FileReader_init(%struct.ttf_reader*, i8 zeroext, i8 zeroext, i8 zeroext, i8*) #3 {
  %6 = alloca %struct.ttf_reader*, align 8
  %7 = alloca i8, align 1
  %8 = alloca i8, align 1
  %9 = alloca i8, align 1
  %10 = alloca i8*, align 8
  %11 = alloca %struct.ttf_reader*, align 8
  store %struct.ttf_reader* %0, %struct.ttf_reader** %6, align 8
  store i8 %1, i8* %7, align 1
  store i8 %2, i8* %8, align 1
  store i8 %3, i8* %9, align 1
  store i8* %4, i8** %10, align 8
  %12 = load %struct.ttf_reader*, %struct.ttf_reader** %6, align 8
  %13 = load i8, i8* %7, align 1
  %14 = zext i8 %13 to i64
  %15 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %12, i64 %14
  store %struct.ttf_reader* %15, %struct.ttf_reader** %11, align 8
  %16 = load i8*, i8** %10, align 8
  %17 = load %struct.ttf_reader*, %struct.ttf_reader** %11, align 8
  %18 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %17, i32 0, i32 14
  store i8* %16, i8** %18, align 8
  %19 = load i8, i8* %8, align 1
  %20 = zext i8 %19 to i64
  %21 = load %struct.ttf_reader*, %struct.ttf_reader** %11, align 8
  %22 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %21, i32 0, i32 8
  store i64 %20, i64* %22, align 8
  %23 = load i8, i8* %9, align 1
  %24 = zext i8 %23 to i64
  %25 = load %struct.ttf_reader*, %struct.ttf_reader** %11, align 8
  %26 = getelementptr inbounds %struct.ttf_reader, %struct.ttf_reader* %25, i32 0, i32 9
  store i64 %24, i64* %26, align 8
  ret i32 0
}

attributes #0 = { alwaysinline uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind readnone speculatable }
attributes #2 = { "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { alwaysinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nounwind }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 8.0.1-9 (tags/RELEASE_801/final)"}
