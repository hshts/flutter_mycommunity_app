"""
一键初始化 GoodPrice 和评论测试数据
"""
import subprocess
import sys

def run_script(script_name, description):
    """运行脚本"""
    print("\n" + "=" * 70)
    print(f"🚀 {description}")
    print("=" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd='.',
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} 完成")
            return True
        else:
            print(f"❌ {description} 失败")
            return False
    except Exception as e:
        print(f"❌ 运行出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("🎯 GoodPrice 测试数据初始化工具")
    print("=" * 70)
    print("\n本脚本将:")
    print("  1. 创建 GoodPrice 商品测试数据")
    print("  2. 为商品添加评论、回复、点赞数据")
    print("  3. 验证 commentid 使用 Integer 类型")
    
    response = input("\n是否继续? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ 已取消")
        return
    
    # 步骤1: 创建商品数据
    success = run_script('init_goodprice_data.py', '步骤1: 创建商品数据')
    if not success:
        print("\n⚠️  商品数据创建可能失败或被取消")
    
    # 步骤2: 创建评论数据
    success = run_script('init_goodprice_comments.py', '步骤2: 创建评论数据')
    if not success:
        print("\n⚠️  评论数据创建失败")
        return
    
    print("\n" + "=" * 70)
    print("🎉 所有测试数据初始化完成!")
    print("=" * 70)
    print("\n✅ 已创建:")
    print("   - GoodPrice 商品数据")
    print("   - GoodPriceComment 评论数据 (commentid 使用 Integer)")
    print("   - GoodPriceCommentReply 回复数据")
    print("   - GoodPriceCommentLike 点赞数据")
    
    print("\n🧪 测试 API:")
    print("   curl 'http://127.0.0.1:5000/grouppurchase/getEvaluateGoodPriceList' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"goodpriceid\":\"[商品ID]\",\"currentIndex\":0}'")
    print("\n💡 查看更多测试建议,请查看脚本输出")
    print("=" * 70)

if __name__ == '__main__':
    main()
