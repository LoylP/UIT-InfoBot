import Image from "next/image";
import Link from "next/link";
import uitImg from "../assets/uit.png";
import robotGif from "../assets/robot.gif";
import background from "../assets/background.png";

export default function Home() {
  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="absolute top-[5%] left-[2%] z-10">
        <Image 
          src={uitImg} 
          alt="UIT Logo" 
          width={96} 
          height={96} 
          className="w-auto h-auto"
        />
      </div>

      {/* Robot */}
      <div className="absolute top-1/2 left-[-4%] transform -translate-y-1/2 scale-75">
        <Image
          src={robotGif}
          alt="Robot"
          width={96}
          height={96}
          className="w-auto h-auto"
        />
      </div>

      {/* Background */}
      <div className="absolute top-0 right-0 w-[60%] h-full">
        <Image
          src={background}
          alt="Background"
          fill
          className="object-cover"
          priority
        />
      </div>

      {/* Content */}
      <div className="absolute right-[6%] top-[20%] z-30 max-w-[450px]">
        <div className="text-[#2C5A87]">
          <p className="font-bold text-[35px]">Xin chào,</p>
          <p className="font-bold text-[28px]">Đậu Đậu có thể giúp gì cho bạn?</p>
          <p className="font-['Baloo_Da_2'] text-[18px] text-justify leading-relaxed mt-[35px]">
            Hãy để Đậu Đậu đồng hành cùng bạn trên hành trình chinh phục tri thức 
            và khám phá môi trường học tập lý tưởng tại Trường Đại học Công nghệ Thông tin!
          </p>
        </div>
      </div>

      {/* Start Button */}
      <Link
        href="/chat"
        className="absolute bottom-[10%] right-[5%] z-20 
                 rounded-[41.5px] font-['Baloo_Da'] text-[28px] 
                 text-white bg-[#2C5A87] px-8 py-3
                 hover:bg-[#0D2849] transition-colors duration-300 font-bold"
      >
        Đặt câu hỏi ngay thôi !!!
      </Link>

      {/* Information Buttons */}
      <div className="absolute left-[2%] bottom-[5%] flex gap-5">
        <Link
          href="https://tuyensinh.uit.edu.vn/truong-dai-hoc-cong-nghe-thong-tin-dhqg-hcm"
          target="_blank"
          rel="noopener noreferrer">
          <button
            className="px-[35px] py-[10px] rounded-[41.5px] 
                      font-['Baloo_Da_2'] text-[18px] text-[#2C5A87] 
                      bg-[#E0EBF2] shadow-md shadow-blue-900 
                      hover:shadow-blue-950 hover:bg-sky-200 hover:font-bold"
          >
            Thông tin
          </button>
        </Link>
        <Link
          href="https://www.uit.edu.vn/lien-he"
          target="_blank"
          rel="noopener noreferrer">
          <button
            className="px-[35px] py-[10px] rounded-[41.5px] 
                      font-['Baloo_Da_2'] text-[18px] text-[#2C5A87] 
                      bg-[#E0EBF2] shadow-md shadow-blue-900 
                      hover:shadow-blue-950 hover:bg-sky-200 hover:font-bold"
          >
            Liên hệ
          </button>
        </Link>
        
      </div>
    </div>
  );
}