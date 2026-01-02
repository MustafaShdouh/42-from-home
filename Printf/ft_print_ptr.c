/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_ptr.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/18 18:30:54 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/30 21:30:22 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_put_ptr(uintptr_t num)
{
	int	len;

	len = 0;
	if (num >= 16)
	{
		len += ft_put_ptr(num / 16);
		len += ft_put_ptr(num % 16);
	}
	else
	{
		if (num < 10)
			len += ft_print_char(num + '0');
		else
			len += ft_print_char(num - 10 + 'a');
	}
	return (len);
}

int	ft_print_ptr(unsigned long long ptr)
{
	int	len;

	len = 0;
	if (ptr == 0)
		return (write(1, "(nil)", 5));
	len += write(1, "0x", 2);
	len += ft_put_ptr(ptr);
	return (len);
}
